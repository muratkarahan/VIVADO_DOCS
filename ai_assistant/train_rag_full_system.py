"""
Vivado FPGA Expert - TAM SİSTEM RAG EĞİTİMİ
Bu script bilgisayardaki TÜM Vivado/FPGA dokümanlarını bulup işler:
1. Xilinx Kurulum Dizini (C:\Xilinx\) - Vivado, Vitis, Data
2. GitHub FPGA Projeleri (docs_fpga, ax7010, z7lite, z7nano, vb.)
3. VIVADO_DOCS workspace'deki tüm dokümanlar
"""

import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm
import tiktoken
import json
from datetime import datetime
import hashlib

# PDF işleme
try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    print("⚠️ PyPDF2 yüklü değil. pip install PyPDF2")
    PDF_AVAILABLE = False


class FullSystemRAGTrainer:
    """Tüm sistemdeki Vivado/FPGA dokümanlarını RAG'e ekler"""
    
    # Aranacak dizinler
    SEARCH_PATHS = [
        "C:/Xilinx/2025.1/Vivado",
        "C:/Xilinx/2025.1/Vitis", 
        "C:/Xilinx/2025.1/data",
        "C:/Users/murat/Documents/GitHub/docs_fpga",
        "C:/Users/murat/Documents/GitHub/ax7010_fpga",
        "C:/Users/murat/Documents/GitHub/z7lite_fpga",
        "C:/Users/murat/Documents/GitHub/z7nano_fpga",
        "C:/Users/murat/Documents/GitHub/coraz7_fpga",
        "C:/Users/murat/Documents/GitHub/nexsys_fpga",
        "C:/Users/murat/Documents/GitHub/VIVADO_DOCS",
    ]
    
    def __init__(self, db_path="./vivado_vectordb_full"):
        load_dotenv()
        self.db_path = db_path
        
        # OpenAI setup
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY bulunamadı!")
        
        self.client = OpenAI(api_key=api_key)
        
        # ChromaDB setup
        print(f"🔧 ChromaDB başlatılıyor: {db_path}")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-ada-002"
        )
        
        # Collection
        self.collection_name = "vivado_full_system"
        try:
            self.collection = self.chroma_client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            print(f"✅ Mevcut collection: {self.collection.count()} döküman")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Full System Vivado/FPGA Documentation"}
            )
            print("🆕 Yeni collection oluşturuldu")
        
        # Tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # İstatistikler
        self.stats = {
            'pdf_count': 0,
            'md_count': 0,
            'txt_count': 0,
            'verilog_count': 0,
            'vhdl_count': 0,
            'total_chunks': 0,
            'total_tokens': 0,
            'failed_files': [],
            'processed_hashes': set(),  # Duplicate kontrolü
            'sources': {},  # Hangi kaynaktan kaç döküman
            'start_time': datetime.now()
        }
    
    def get_file_hash(self, filepath):
        """Dosya içeriğinin hash'ini al (duplicate kontrolü için)"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def count_tokens(self, text):
        """Token sayısı"""
        return len(self.tokenizer.encode(text))
    
    def chunk_text(self, text, chunk_size=1000, overlap=200):
        """Metni akıllı chunk'lara böl"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = self.count_tokens(para)
            
            if para_tokens > chunk_size:
                lines = para.split('\n')
                for line in lines:
                    line_tokens = self.count_tokens(line)
                    
                    if current_tokens + line_tokens > chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = line + '\n'
                        current_tokens = line_tokens
                    else:
                        current_chunk += line + '\n'
                        current_tokens += line_tokens
            else:
                if current_tokens + para_tokens > chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = para + '\n\n'
                    current_tokens = para_tokens
                else:
                    current_chunk += para + '\n\n'
                    current_tokens += para_tokens
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def extract_pdf_text(self, pdf_path):
        """PDF'den text çıkar"""
        if not PDF_AVAILABLE:
            return None
        
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"   ❌ PDF okuma hatası: {e}")
            return None
    
    def find_all_documents(self):
        """Tüm sistemi tara, dokümanları bul"""
        all_files = {'pdf': [], 'md': [], 'txt': [], 'verilog': [], 'vhdl': []}
        
        print("\n🔍 Sistem taranıyor...")
        
        for search_path in self.SEARCH_PATHS:
            path = Path(search_path)
            if not path.exists():
                continue
            
            print(f"   📁 {search_path}")
            
            # PDF'ler
            pdfs = list(path.rglob("*.pdf"))
            all_files['pdf'].extend(pdfs)
            
            # Markdown
            mds = list(path.rglob("*.md"))
            all_files['md'].extend(mds)
            
            # Text
            txts = list(path.rglob("*.txt"))
            all_files['txt'].extend(txts)
            
            # Verilog/SystemVerilog (sadece templates ve examples)
            if "Vivado" in str(path):
                for ext in ["*.v", "*.vh", "*.sv"]:
                    v_files = path.rglob(ext)
                    # Sadece örnek ve template dosyalarını al
                    all_files['verilog'].extend([f for f in v_files 
                        if any(x in str(f).lower() for x in ['template', 'example', 'demo', 'samples'])])
            
            # VHDL (sadece templates ve examples)
            if "Vivado" in str(path):
                vhdl_files = path.rglob("*.vhd")
                all_files['vhdl'].extend([f for f in vhdl_files 
                    if any(x in str(f).lower() for x in ['template', 'example', 'demo', 'samples'])])
        
        return all_files
    
    def add_document_to_db(self, text, metadata):
        """Dokümanı ChromaDB'ye ekle (hata toleranslı)"""
        chunks = self.chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            doc_id = f"{metadata['source']}_{metadata['filename']}_{i}"
            chunk_metadata = {
                **metadata,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'tokens': self.count_tokens(chunk)
            }
            
            try:
                self.collection.add(
                    documents=[chunk],
                    metadatas=[chunk_metadata],
                    ids=[doc_id]
                )
                
                self.stats['total_chunks'] += 1
                self.stats['total_tokens'] += chunk_metadata['tokens']
            except Exception as e:
                print(f"\n   ⚠️ Chunk {i} eklenemedi: {str(e)[:100]}")
                self.stats['failed_files'].append(f"{metadata['filename']}_chunk{i}")
                # İnternet hatası varsa bekle ve tekrar dene
                if "Connection" in str(e) or "timeout" in str(e).lower():
                    import time
                    print("   ⏳ 5 saniye bekleniyor...")
                    time.sleep(5)
                    try:
                        self.collection.add(
                            documents=[chunk],
                            metadatas=[chunk_metadata],
                            ids=[doc_id]
                        )
                        self.stats['total_chunks'] += 1
                        self.stats['total_tokens'] += chunk_metadata['tokens']
                    except:
                        pass
        
        return len(chunks)
    
    def process_pdf(self, pdf_path, source_name):
        """PDF işle"""
        file_hash = self.get_file_hash(pdf_path)
        if file_hash in self.stats['processed_hashes']:
            return 0  # Duplicate, skip
        
        text = self.extract_pdf_text(pdf_path)
        if not text or len(text.strip()) < 100:
            return 0
        
        metadata = {
            'source': source_name,
            'filename': pdf_path.name,
            'filepath': str(pdf_path),
            'type': 'pdf',
            'hash': file_hash
        }
        
        chunks = self.add_document_to_db(text, metadata)
        self.stats['processed_hashes'].add(file_hash)
        self.stats['pdf_count'] += 1
        
        return chunks
    
    def process_markdown(self, md_path, source_name):
        """Markdown işle"""
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            file_hash = hashlib.md5(text.encode()).hexdigest()
            if file_hash in self.stats['processed_hashes']:
                return 0
            
            metadata = {
                'source': source_name,
                'filename': md_path.name,
                'filepath': str(md_path),
                'type': 'markdown',
                'hash': file_hash
            }
            
            chunks = self.add_document_to_db(text, metadata)
            self.stats['processed_hashes'].add(file_hash)
            self.stats['md_count'] += 1
            
            return chunks
        except:
            return 0
    
    def process_verilog(self, v_path, source_name):
        """Verilog/SystemVerilog işle"""
        try:
            with open(v_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            file_hash = hashlib.md5(text.encode()).hexdigest()
            if file_hash in self.stats['processed_hashes']:
                return 0
            
            metadata = {
                'source': source_name,
                'filename': v_path.name,
                'filepath': str(v_path),
                'type': 'verilog',
                'hash': file_hash
            }
            
            chunks = self.add_document_to_db(text, metadata)
            self.stats['processed_hashes'].add(file_hash)
            self.stats['verilog_count'] += 1
            
            return chunks
        except:
            return 0
    
    def process_vhdl(self, vhd_path, source_name):
        """VHDL işle"""
        try:
            with open(vhd_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            file_hash = hashlib.md5(text.encode()).hexdigest()
            if file_hash in self.stats['processed_hashes']:
                return 0
            
            metadata = {
                'source': source_name,
                'filename': vhd_path.name,
                'filepath': str(vhd_path),
                'type': 'vhdl',
                'hash': file_hash
            }
            
            chunks = self.add_document_to_db(text, metadata)
            self.stats['processed_hashes'].add(file_hash)
            self.stats['vhdl_count'] += 1
            
            return chunks
        except:
            return 0
    
    def train_full_system(self):
        """Tüm sistemi tara ve eğit"""
        print("=" * 80)
        print("🚀 TAM SİSTEM RAG EĞİTİMİ")
        print("=" * 80)
        
        # Dokümanları bul
        all_files = self.find_all_documents()
        
        total_files = (len(all_files['pdf']) + len(all_files['md']) + 
                      len(all_files['txt']) + len(all_files['verilog']) + len(all_files['vhdl']))
        print(f"\n📊 Toplam Dosya: {total_files}")
        print(f"   📄 PDF: {len(all_files['pdf'])}")
        print(f"   📝 Markdown: {len(all_files['md'])}")
        print(f"   📄 Text: {len(all_files['txt'])}")
        print(f"   🔧 Verilog: {len(all_files['verilog'])}")
        print(f"   🔧 VHDL: {len(all_files['vhdl'])}")
        
        # PDF'leri işle
        if all_files['pdf']:
            print("\n" + "-" * 80)
            print("📄 PDF DOSYALARI İŞLENİYOR")
            print("-" * 80)
            
            for pdf_path in tqdm(all_files['pdf'], desc="PDF'ler"):
                # Kaynağı belirle
                source = "unknown"
                path_str = str(pdf_path)
                if "Xilinx" in path_str:
                    if "Vivado" in path_str:
                        source = "xilinx_vivado"
                    elif "Vitis" in path_str:
                        source = "xilinx_vitis"
                    elif "data" in path_str:
                        source = "xilinx_data"
                elif "docs_fpga" in path_str:
                    source = "docs_fpga"
                elif "ax7010" in path_str:
                    source = "ax7010_project"
                elif "z7lite" in path_str:
                    source = "z7lite_project"
                elif "z7nano" in path_str:
                    source = "z7nano_project"
                elif "VIVADO_DOCS" in path_str:
                    source = "vivado_docs_workspace"
                
                chunks = self.process_pdf(pdf_path, source)
                
                # İstatistik güncelle
                if source not in self.stats['sources']:
                    self.stats['sources'][source] = 0
                self.stats['sources'][source] += 1
        
        # Markdown'ları işle
        if all_files['md']:
            print("\n" + "-" * 80)
            print("📝 MARKDOWN DOSYALARI İŞLENİYOR")
            print("-" * 80)
            
            for md_path in tqdm(all_files['md'], desc="Markdown'lar"):
                source = "markdown_docs"
                if "VIVADO_DOCS" in str(md_path):
                    source = "vivado_docs_workspace"
                
                chunks = self.process_markdown(md_path, source)
                
                if source not in self.stats['sources']:
                    self.stats['sources'][source] = 0
                if chunks > 0:
                    self.stats['sources'][source] += 1
        
        # Verilog dosyalarını işle
        if all_files['verilog']:
            print("\n" + "-" * 80)
            print("🔧 VERILOG TEMPLATE VE ÖRNEKLER İŞLENİYOR")
            print("-" * 80)
            
            for v_path in tqdm(all_files['verilog'], desc="Verilog"):
                source = "vivado_verilog_templates"
                chunks = self.process_verilog(v_path, source)
                
                if source not in self.stats['sources']:
                    self.stats['sources'][source] = 0
                if chunks > 0:
                    self.stats['sources'][source] += 1
        
        # VHDL dosyalarını işle
        if all_files['vhdl']:
            print("\n" + "-" * 80)
            print("🔧 VHDL TEMPLATE VE ÖRNEKLER İŞLENİYOR")
            print("-" * 80)
            
            for vhd_path in tqdm(all_files['vhdl'], desc="VHDL"):
                source = "vivado_vhdl_templates"
                chunks = self.process_vhdl(vhd_path, source)
                
                if source not in self.stats['sources']:
                    self.stats['sources'][source] = 0
                if chunks > 0:
                    self.stats['sources'][source] += 1
        
        # Sonuçları göster
        self.show_results()
    
    def show_results(self):
        """Eğitim sonuçlarını göster"""
        duration = (datetime.now() - self.stats['start_time']).total_seconds()
        embedding_cost = (self.stats['total_tokens'] / 1000) * 0.0001
        
        print("\n" + "=" * 80)
        print("✅ TAM SİSTEM RAG EĞİTİMİ TAMAMLANDI")
        print("=" * 80)
        
        print(f"\n📊 İstatistikler:")
        print(f"   ⏱️  Süre: {duration:.1f} saniye")
        print(f"   📄 PDF: {self.stats['pdf_count']} dosya")
        print(f"   📝 Markdown: {self.stats['md_count']} dosya")
        print(f"   � Verilog: {self.stats['verilog_count']} dosya")
        print(f"   🔧 VHDL: {self.stats['vhdl_count']} dosya")
        print(f"   �📚 Toplam Chunk: {self.stats['total_chunks']}")
        print(f"   🔢 Toplam Token: {self.stats['total_tokens']:,}")
        print(f"   💾 Database: {self.collection.count()} döküman")
        print(f"   💰 Tahmini Maliyet: ${embedding_cost:.4f}")
        
        print(f"\n📂 Kaynaklar:")
        for source, count in sorted(self.stats['sources'].items()):
            print(f"   • {source}: {count} dosya")
        
        if self.stats['failed_files']:
            print(f"\n⚠️ Başarısız: {len(self.stats['failed_files'])} dosya")
        
        print("=" * 80)
        
        # İstatistikleri kaydet
        stats_file = Path(self.db_path) / "full_training_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump({
                'duration_seconds': duration,
                'pdf_count': self.stats['pdf_count'],
                'md_count': self.stats['md_count'],
                'verilog_count': self.stats['verilog_count'],
                'vhdl_count': self.stats['vhdl_count'],
                'total_chunks': self.stats['total_chunks'],
                'total_tokens': self.stats['total_tokens'],
                'embedding_cost': embedding_cost,
                'sources': self.stats['sources'],
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n📝 İstatistikler kaydedildi: {stats_file}")
        print("\n✨ Artık 'python vivado_agent.py' ile asistanı kullanabilirsiniz!")


def main():
    """Ana fonksiyon"""
    try:
        trainer = FullSystemRAGTrainer()
        trainer.train_full_system()
    except KeyboardInterrupt:
        print("\n\n⚠️ Kullanıcı tarafından iptal edildi")
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
