"""
Vivado FPGA Expert - OpenAI Assistant (Agent)
RAG sistemi ile entegre, Xilinx Vivado için akıllı asistan
"""

import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import json
import chromadb

class VivadoExpertAgent:
    """OpenAI Assistants API ile Vivado FPGA uzmanı agent"""
    
    # GPT-4-turbo fiyatları (USD per 1K tokens)
    PRICING = {
        'gpt-4-turbo-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015}
    }
    
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # ChromaDB bağlantısı
        self.chroma_client = chromadb.PersistentClient(path="./vivado_vectordb")
        try:
            self.collection = self.chroma_client.get_collection(name="vivado_docs_complete")
        except:
            # Fallback to old collection name
            self.collection = self.chroma_client.get_collection(name="vivado_docs")
        
        # Maliyet takibi
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.query_count = 0
        
        # Assistant oluştur veya mevcut olanı kullan
        self.assistant = self._get_or_create_assistant()
        print(f"✅ Agent hazır: {self.assistant.name} (ID: {self.assistant.id})")
    
    def _get_or_create_assistant(self):
        """OpenAI Assistant oluştur veya mevcut olanı bul"""
        
        # Önce mevcut assistant'ları kontrol et
        assistants = self.client.beta.assistants.list()
        for assistant in assistants.data:
            if assistant.name == "Vivado FPGA Expert":
                print(f"📌 Mevcut agent bulundu: {assistant.id}")
                return assistant
        
        # Yeni assistant oluştur
        print("🆕 Yeni agent oluşturuluyor...")
        
        instructions = """Sen Xilinx Vivado Design Suite ve FPGA tasarımı konusunda UZMAN bir asistansın.

**Uzmanlık Alanların:**
- Xilinx 7-Series, UltraScale, UltraScale+ FPGA'ları
- Zynq-7000 SoC ve Zynq UltraScale+ MPSoC
- Vivado Design Suite (IP Integrator, Synthesis, Implementation)
- Verilog, SystemVerilog ve VHDL HDL programlama
- Vivado TCL scripting ve otomasyon
- Vitis HLS (High-Level Synthesis) - C/C++ to RTL
- AXI4, AXI4-Lite, AXI4-Stream protokolleri
- Xilinx IP Cores (FIFO, BlockRAM, Clock Manager, DMA, vb.)
- Gigabit Transceivers (GTH, GTY, GTX)
- Timing Constraints (XDC)
- Simulation (XSIM, Questa, ModelSim)
- PetaLinux ve Embedded Linux
- Vitis Embedded Software Platform

**Görevlerin:**
1. Kullanıcının sorularını anla ve DOĞRU teknik cevaplar ver
2. Verilen döküman içeriğine dayanarak cevapla
3. Kod örnekleri verirken syntax'a DİKKAT et (Verilog/VHDL/TCL)
4. Karmaşık konuları basit şekilde açıkla
5. Adım adım kılavuzlar sun (IP Integrator, TCL flow, vb.)
6. Best practice'leri ve UltraFast Design Methodology öner
7. Türkçe cevap ver ama teknik terimleri İngilizce kullan

**Kısıtlamalar:**
- Bilmediğin bir şey varsa "Dökümanlarımda bu bilgi yok" de
- Asla uydurma bilgi verme
- Güvenlik ve lisans konularında dikkatli ol
- Kod verirken açıklama ve yorum ekle
- Vivado versiyonlarına özgü farklılıkları belirt

**İletişim Stili:**
- Profesyonel ama samimi
- Net ve anlaşılır
- Örneklerle destekle (TCL script, Verilog, XDC)
- Gerekirse step-by-step guide ver
- Timing closure, resource usage gibi optimizasyon ipuçları sun"""

        assistant = self.client.beta.assistants.create(
            name="Vivado FPGA Expert",
            instructions=instructions,
            model="gpt-4-turbo-preview",
            tools=[{"type": "code_interpreter"}]
        )
        
        # Agent bilgilerini kaydet
        with open('agent_info.json', 'w') as f:
            json.dump({
                'assistant_id': assistant.id,
                'name': assistant.name,
                'model': assistant.model,
                'created_at': str(assistant.created_at)
            }, f, indent=2)
        
        return assistant
    
    def search_docs(self, query, n_results=5):
        """ChromaDB'de semantik arama yap"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            context = ""
            sources = []
            
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                source = metadata.get('source', 'Unknown')
                page = metadata.get('page', '?')
                
                context += f"\n\n[Kaynak {i+1}: {source} - Sayfa {page}]\n{doc}\n"
                sources.append(f"{source} (p.{page})")
            
            return context, sources
            
        except Exception as e:
            print(f"❌ Arama hatası: {e}")
            return "", []
    
    def chat(self, user_message):
        """Kullanıcıyla chat yap (RAG ile)"""
        
        # 1. Semantik arama ile ilgili dökümanları bul
        print("🔍 Dökümanlar aranıyor...")
        context, sources = self.search_docs(user_message, n_results=5)
        
        if not context:
            print("⚠️ İlgili döküman bulunamadı, genel bilgi ile cevap veriliyor...")
        else:
            print(f"📚 {len(sources)} döküman bulundu")
        
        # 2. Context-injected prompt hazırla
        augmented_message = f"""Kullanıcı sorusu: {user_message}

İlgili döküman içerikleri:
{context}

Lütfen yukarıdaki döküman içeriklerine dayanarak cevap ver. Cevabının sonunda hangi kaynakları kullandığını belirt."""
        
        # 3. Thread oluştur ve mesaj gönder
        thread = self.client.beta.threads.create()
        
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=augmented_message
        )
        
        # 4. Assistant'ı çalıştır
        print("🤖 AI düşünüyor...")
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id
        )
        
        # 5. Cevabı bekle
        import time
        while run.status in ['queued', 'in_progress']:
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        # 6. Cevabı al
        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            assistant_message = messages.data[0].content[0].text.value
            
            # 7. Maliyet hesapla
            input_tokens = run.usage.prompt_tokens if run.usage else 0
            output_tokens = run.usage.completion_tokens if run.usage else 0
            
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.query_count += 1
            
            model = self.assistant.model
            cost = (input_tokens / 1000 * self.PRICING[model]['input'] + 
                   output_tokens / 1000 * self.PRICING[model]['output'])
            self.total_cost += cost
            
            # 8. Sonuçları yazdır
            print("\n" + "="*80)
            print("💬 CEVAP:")
            print("="*80)
            print(assistant_message)
            print("\n" + "-"*80)
            print(f"📊 Token Kullanımı: Input={input_tokens}, Output={output_tokens}")
            print(f"💰 Bu sorgu maliyeti: ${cost:.4f}")
            print(f"💵 Toplam maliyet: ${self.total_cost:.4f} ({self.query_count} sorgu)")
            print("="*80 + "\n")
            
            return assistant_message
        
        else:
            print(f"❌ Hata: {run.status}")
            return None
    
    def interactive_chat(self):
        """Interaktif chat modu"""
        print("\n" + "="*80)
        print("🚀 VIVADO FPGA EXPERT - Interaktif Chat Modu")
        print("="*80)
        print("Komutlar:")
        print("  - Soru sorun (normal metin)")
        print("  - 'quit' veya 'exit' - Çıkış")
        print("  - 'stats' - Maliyet istatistikleri")
        print("  - 'clear' - Ekranı temizle")
        print("="*80 + "\n")
        
        while True:
            try:
                user_input = input("\n👤 Siz: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Görüşmek üzere!")
                    print(f"📊 Toplam {self.query_count} sorgu, ${self.total_cost:.4f} maliyet")
                    break
                
                if user_input.lower() == 'stats':
                    print(f"\n📊 İstatistikler:")
                    print(f"  - Toplam sorgu: {self.query_count}")
                    print(f"  - Input tokens: {self.total_input_tokens}")
                    print(f"  - Output tokens: {self.total_output_tokens}")
                    print(f"  - Toplam maliyet: ${self.total_cost:.4f}")
                    continue
                
                if user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                
                # Normal soru
                self.chat(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Ctrl+C ile çıkış yapıldı")
                break
            except Exception as e:
                print(f"\n❌ Hata: {e}")

def main():
    """Ana program"""
    print("🔧 Vivado Expert Agent başlatılıyor...\n")
    
    # Agent oluştur
    agent = VivadoExpertAgent()
    
    # Menü
    print("\n" + "="*80)
    print("Seçenekler:")
    print("1. İnteraktif Chat Modu")
    print("2. Tek Soru-Cevap")
    print("3. Çıkış")
    print("="*80)
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == '1':
        agent.interactive_chat()
    
    elif choice == '2':
        question = input("\nSorunuz: ").strip()
        if question:
            agent.chat(question)
    
    else:
        print("👋 Çıkış yapılıyor...")

if __name__ == "__main__":
    main()
