"""
Vivado FPGA Expert - Tam RAG Eğitim Sistemi
Tüm dokümanları (PDF, MD, TXT) işleyip vector database'e ekler
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

# PDF işleme için
try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    print("⚠️ PyPDF2 yüklü değil. PDF desteği kapalı.")
    PDF_AVAILABLE = False

class VivadoRAGTrainer:
    """Vivado dokümanlarını tam RAG sistemi için hazırlayan sınıf"""
    
    def __init__(self, 
                 workspace_dir="c:/Users/murat/Documents/GitHub/VIVADO_DOCS",
                 db_path="./vivado_vectordb"):
        load_dotenv()
        self.workspace_dir = Path(workspace_dir)
        self.db_path = db_path
        
        # OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        self.client = OpenAI(api_key=api_key)
        
        # ChromaDB setup
        print(f"🔧 ChromaDB başlatılıyor: {db_path}")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        # OpenAI embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-ada-002"
        )
        
        # Collection oluştur veya al
        self.collection_name = "vivado_docs_complete"
        try:
            self.collection = self.chroma_client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            print(f"✅ Mevcut collection bulundu: {self.collection.count()} döküman")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Xilinx Vivado Complete Documentation (PDF+MD+TXT)"}
            )
            print("🆕 Yeni collection oluşturuldu")
        
        # Tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # İstatistikler
        self.stats = {
            'pdf_count': 0,
            'md_count': 0,
            'txt_count': 0,
            'total_chunks': 0,
            'total_tokens': 0,
            'failed_files': [],
            'start_time': datetime.now()
        }
    
    def count_tokens(self, text):
        """Text'in token sayısını hesapla"""
        return len(self.tokenizer.encode(text))
    
    def chunk_text(self, text, chunk_size=1000, overlap=200):
        """Metni chunk'lara böl (token-based, akıllı bölme)"""
        # Önce paragraflara böl
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = self.count_tokens(para)
            
            # Eğer paragraf çok büyükse satırlara böl
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
            
            # Normal paragraf
            elif current_tokens + para_tokens > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + '\n\n'
                current_tokens = para_tokens
            else:
                current_chunk += para + '\n\n'
                current_tokens += para_tokens
        
        # Son chunk'ı ekle
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def process_markdown(self, md_path):
        """Markdown dosyasını işle"""
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if not text.strip():
                return 0
            
            print(f"\n📝 {md_path.name}")
            
            # Chunk'lara böl
            chunks = self.chunk_text(text, chunk_size=1000, overlap=150)
            
            if not chunks:
                return 0
            
            all_metadata = []
            for chunk_idx, chunk in enumerate(chunks):
                all_metadata.append({
                    'source': md_path.name,
                    'file_path': str(md_path.relative_to(self.workspace_dir)),
                    'chunk': chunk_idx,
                    'doc_type': self._get_doc_type(md_path),
                    'file_type': 'markdown'
                })
            
            # Unique ID'ler oluştur
            ids = [f"{md_path.stem}_md_c{m['chunk']}" for m in all_metadata]
            
            # ChromaDB'ye ekle
            self.collection.add(
                documents=chunks,
                metadatas=all_metadata,
                ids=ids
            )
            
            print(f"   ✅ {len(chunks)} chunk eklendi")
            self.stats['md_count'] += 1
            self.stats['total_chunks'] += len(chunks)
            self.stats['total_tokens'] += sum(self.count_tokens(c) for c in chunks)
            
            return len(chunks)
            
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            self.stats['failed_files'].append(str(md_path))
            return 0
    
    def process_pdf(self, pdf_path):
        """PDF dosyasını işle"""
        if not PDF_AVAILABLE:
            print(f"   ⚠️ PDF desteği yok, atlanıyor: {pdf_path.name}")
            return 0
            
        try:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            print(f"\n📄 {pdf_path.name}")
            print(f"   Sayfa sayısı: {total_pages}")
            
            all_chunks = []
            all_metadata = []
            
            for page_num in tqdm(range(total_pages), desc="   Sayfa işleniyor"):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                if not text.strip():
                    continue
                
                # Chunk'lara böl
                chunks = self.chunk_text(text, chunk_size=800, overlap=150)
                
                for chunk_idx, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_metadata.append({
                        'source': pdf_path.name,
                        'file_path': str(pdf_path.relative_to(self.workspace_dir)),
                        'page': page_num + 1,
                        'chunk': chunk_idx,
                        'doc_type': self._get_doc_type(pdf_path),
                        'file_type': 'pdf'
                    })
            
            # ChromaDB'ye ekle
            if all_chunks:
                ids = [f"{pdf_path.stem}_p{m['page']}_c{m['chunk']}" for m in all_metadata]
                
                self.collection.add(
                    documents=all_chunks,
                    metadatas=all_metadata,
                    ids=ids
                )
                
                print(f"   ✅ {len(all_chunks)} chunk eklendi")
                self.stats['pdf_count'] += 1
                self.stats['total_chunks'] += len(all_chunks)
                self.stats['total_tokens'] += sum(self.count_tokens(c) for c in all_chunks)
                
                return len(all_chunks)
            else:
                print(f"   ⚠️ Metin çıkarılamadı")
                return 0
                
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            self.stats['failed_files'].append(str(pdf_path))
            return 0
    
    def process_txt(self, txt_path):
        """TXT dosyasını işle"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if not text.strip():
                return 0
            
            print(f"\n📄 {txt_path.name}")
            
            chunks = self.chunk_text(text, chunk_size=1000, overlap=150)
            
            if not chunks:
                return 0
            
            all_metadata = []
            for chunk_idx, chunk in enumerate(chunks):
                all_metadata.append({
                    'source': txt_path.name,
                    'file_path': str(txt_path.relative_to(self.workspace_dir)),
                    'chunk': chunk_idx,
                    'doc_type': self._get_doc_type(txt_path),
                    'file_type': 'text'
                })
            
            ids = [f"{txt_path.stem}_txt_c{m['chunk']}" for m in all_metadata]
            
            self.collection.add(
                documents=chunks,
                metadatas=all_metadata,
                ids=ids
            )
            
            print(f"   ✅ {len(chunks)} chunk eklendi")
            self.stats['txt_count'] += 1
            self.stats['total_chunks'] += len(chunks)
            self.stats['total_tokens'] += sum(self.count_tokens(c) for c in chunks)
            
            return len(chunks)
            
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            self.stats['failed_files'].append(str(txt_path))
            return 0
    
    def _get_doc_type(self, file_path):
        """Dosya türünü klasör yapısından çıkar"""
        parts = file_path.parts
        
        if 'official_docs' in parts:
            idx = parts.index('official_docs')
            if idx + 1 < len(parts):
                return f"Official/{parts[idx+1]}"
            return "Official/General"
        elif 'code_examples' in parts:
            return "CodeExamples"
        elif 'vivado-examples' in parts:
            return "VivadoExamples"
        elif 'ai_assistant' in parts:
            return "AIAssistant"
        else:
            return "General"
    
    def train_all(self, skip_patterns=None):
        """Tüm dokümanları işle ve RAG için hazırla"""
        print("\n" + "="*80)
        print("🚀 VIVADO RAG TAM EĞİTİM SİSTEMİ")
        print("="*80)
        print(f"📂 Workspace: {self.workspace_dir}")
        print(f"💾 Database: {self.db_path}")
        
        if skip_patterns is None:
            skip_patterns = [
                'node_modules',
                '.git',
                '__pycache__',
                'vivado_vectordb',
                '.vscode',
                'vscode-extension'
            ]
        
        # Dosyaları topla
        print("\n🔍 Dosyalar taranıyor...")
        
        md_files = []
        pdf_files = []
        txt_files = []
        
        for pattern in ['**/*.md', '**/*.pdf', '**/*.txt']:
            for file_path in self.workspace_dir.rglob(pattern.split('/')[-1]):
                # Skip patterns kontrolü
                if any(skip in str(file_path) for skip in skip_patterns):
                    continue
                
                if file_path.suffix == '.md':
                    md_files.append(file_path)
                elif file_path.suffix == '.pdf':
                    pdf_files.append(file_path)
                elif file_path.suffix == '.txt':
                    txt_files.append(file_path)
        
        total_files = len(md_files) + len(pdf_files) + len(txt_files)
        
        print(f"\n📊 Bulunan Dosyalar:")
        print(f"   📝 Markdown: {len(md_files)}")
        print(f"   📄 PDF: {len(pdf_files)}")
        print(f"   📄 Text: {len(txt_files)}")
        print(f"   📚 Toplam: {total_files}")
        
        if total_files == 0:
            print("\n❌ İşlenecek dosya bulunamadı!")
            return
        
        # Markdown dosyalarını işle
        if md_files:
            print("\n" + "-"*80)
            print("📝 MARKDOWN DOSYALARI İŞLENİYOR")
            print("-"*80)
            for md_file in md_files:
                self.process_markdown(md_file)
        
        # PDF dosyalarını işle
        if pdf_files:
            print("\n" + "-"*80)
            print("📄 PDF DOSYALARI İŞLENİYOR")
            print("-"*80)
            for pdf_file in pdf_files:
                self.process_pdf(pdf_file)
        
        # TXT dosyalarını işle
        if txt_files:
            print("\n" + "-"*80)
            print("📄 TEXT DOSYALARI İŞLENİYOR")
            print("-"*80)
            for txt_file in txt_files:
                self.process_txt(txt_file)
        
        # İstatistikleri göster
        self._print_final_stats()
        
        # İstatistikleri kaydet
        self._save_training_stats()
    
    def _print_final_stats(self):
        """Final istatistiklerini yazdır"""
        end_time = datetime.now()
        duration = (end_time - self.stats['start_time']).total_seconds()
        
        print("\n" + "="*80)
        print("✅ RAG EĞİTİMİ TAMAMLANDI")
        print("="*80)
        print(f"\n📊 İstatistikler:")
        print(f"   ⏱️  Süre: {duration:.1f} saniye")
        print(f"   📝 Markdown: {self.stats['md_count']} dosya")
        print(f"   📄 PDF: {self.stats['pdf_count']} dosya")
        print(f"   📄 Text: {self.stats['txt_count']} dosya")
        print(f"   📚 Toplam Chunk: {self.stats['total_chunks']}")
        print(f"   🔢 Toplam Token: {self.stats['total_tokens']:,}")
        print(f"   💾 Database: {self.collection.count()} döküman")
        
        # Embedding maliyeti (text-embedding-ada-002: $0.0001 / 1K token)
        embedding_cost = (self.stats['total_tokens'] / 1000) * 0.0001
        print(f"   💰 Tahmini Embedding Maliyet: ${embedding_cost:.4f}")
        
        if self.stats['failed_files']:
            print(f"\n⚠️  Başarısız Dosyalar ({len(self.stats['failed_files'])}):")
            for failed in self.stats['failed_files'][:10]:
                print(f"   - {failed}")
            if len(self.stats['failed_files']) > 10:
                print(f"   ... ve {len(self.stats['failed_files']) - 10} dosya daha")
        
        print("="*80 + "\n")
    
    def _save_training_stats(self):
        """Eğitim istatistiklerini kaydet"""
        stats_file = Path(self.db_path) / "training_stats.json"
        
        stats_data = {
            **self.stats,
            'start_time': self.stats['start_time'].isoformat(),
            'end_time': datetime.now().isoformat(),
            'collection_name': self.collection_name,
            'total_documents': self.collection.count()
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        print(f"📝 İstatistikler kaydedildi: {stats_file}")
    
    def test_search(self, queries=None):
        """Eğitilmiş RAG sistemini test et"""
        if queries is None:
            queries = [
                "Vivado nedir ve nasıl kullanılır?",
                "AXI4-Lite interface nasıl oluşturulur?",
                "Zynq PS-PL haberleşmesi",
                "FPGA synthesis optimization",
                "Vivado TCL scripting"
            ]
        
        print("\n" + "="*80)
        print("🧪 RAG SİSTEMİ TEST EDİLİYOR")
        print("="*80)
        
        for query in queries:
            print(f"\n🔍 Sorgu: '{query}'")
            print("-" * 80)
            
            results = self.collection.query(
                query_texts=[query],
                n_results=3
            )
            
            if results['documents'][0]:
                print("📄 Sonuçlar:")
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i]
                    print(f"\n  {i+1}. Kaynak: {metadata['source']}")
                    print(f"     Tür: {metadata['doc_type']} ({metadata['file_type']})")
                    if 'page' in metadata:
                        print(f"     Sayfa: {metadata['page']}")
                    print(f"     İçerik: {doc[:150]}...")
            else:
                print("   ⚠️ Sonuç bulunamadı")
        
        print("\n" + "="*80 + "\n")

def main():
    """Ana program"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Vivado FPGA Expert - Tam RAG Eğitim Sistemi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  # Tüm dokümanları işle
  python train_rag_complete.py
  
  # Collection'ı sıfırdan oluştur
  python train_rag_complete.py --reindex
  
  # Eğitim sonrası test yap
  python train_rag_complete.py --test
  
  # Özel workspace klasörü
  python train_rag_complete.py --workspace "D:/MyVivadoDocs"
        """
    )
    
    parser.add_argument('--workspace', 
                       default='c:/Users/murat/Documents/GitHub/VIVADO_DOCS',
                       help='Workspace klasörü')
    parser.add_argument('--db-path', 
                       default='./vivado_vectordb',
                       help='ChromaDB path')
    parser.add_argument('--reindex', 
                       action='store_true',
                       help='Collection silip yeniden indexle')
    parser.add_argument('--test', 
                       action='store_true',
                       help='Eğitim sonrası test yap')
    parser.add_argument('--skip-patterns',
                       nargs='+',
                       help='Atlanacak klasör/dosya patternleri')
    
    args = parser.parse_args()
    
    try:
        # Trainer oluştur
        trainer = VivadoRAGTrainer(args.workspace, args.db_path)
        
        # Reindex ise mevcut collection'ı sil
        if args.reindex:
            try:
                trainer.chroma_client.delete_collection(trainer.collection_name)
                print("🗑️ Mevcut collection silindi")
                trainer.collection = trainer.chroma_client.create_collection(
                    name=trainer.collection_name,
                    embedding_function=trainer.embedding_function
                )
            except:
                pass
        
        # Tüm dokümanları işle
        trainer.train_all(skip_patterns=args.skip_patterns)
        
        # Test
        if args.test:
            trainer.test_search()
        
        print("\n✨ İşlem tamamlandı!")
        print(f"🎯 Şimdi 'python vivado_agent.py' ile asistanı çalıştırabilirsiniz.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ İşlem kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
