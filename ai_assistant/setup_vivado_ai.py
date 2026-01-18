"""
Vivado Dökümanlarını ChromaDB'ye İndexleme
PDF dosyalarını okur, parçalar, embedler ve vektör database'e yazar
"""

import os
from pathlib import Path
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm
import tiktoken

class VivadoDocsIndexer:
    """Vivado dökümanlarını indexleyen sınıf"""
    
    def __init__(self, docs_dir="../official_docs", db_path="./vivado_vectordb"):
        load_dotenv()
        self.docs_dir = Path(docs_dir)
        self.db_path = db_path
        
        # OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # ChromaDB setup
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        # OpenAI embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="text-embedding-ada-002"
        )
        
        # Collection oluştur veya al
        try:
            self.collection = self.chroma_client.get_collection(
                name="vivado_docs",
                embedding_function=self.embedding_function
            )
            print(f"✅ Mevcut collection bulundu: {self.collection.count()} döküman")
        except:
            self.collection = self.chroma_client.create_collection(
                name="vivado_docs",
                embedding_function=self.embedding_function,
                metadata={"description": "Xilinx Vivado Design Suite Documentation"}
            )
            print("🆕 Yeni collection oluşturuldu")
        
        # Tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text):
        """Text'in token sayısını hesapla"""
        return len(self.tokenizer.encode(text))
    
    def chunk_text(self, text, chunk_size=1000, overlap=200):
        """Metni chunk'lara böl (token-based)"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        i = 0
        while i < len(tokens):
            chunk_tokens = tokens[i:i+chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            i += (chunk_size - overlap)
        
        return chunks
    
    def process_pdf(self, pdf_path):
        """Tek bir PDF'i işle"""
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
                        'page': page_num + 1,
                        'chunk': chunk_idx,
                        'doc_type': self._get_doc_type(pdf_path)
                    })
            
            # ChromaDB'ye ekle
            if all_chunks:
                # Unique ID'ler oluştur
                ids = [f"{pdf_path.stem}_p{m['page']}_c{m['chunk']}" 
                       for m in all_metadata]
                
                self.collection.add(
                    documents=all_chunks,
                    metadatas=all_metadata,
                    ids=ids
                )
                
                print(f"   ✅ {len(all_chunks)} chunk eklendi")
                return len(all_chunks)
            else:
                print(f"   ⚠️ Metin çıkarılamadı")
                return 0
                
        except Exception as e:
            print(f"   ❌ Hata: {e}")
            return 0
    
    def _get_doc_type(self, pdf_path):
        """PDF türünü klasör yapısından çıkar"""
        parts = pdf_path.parts
        
        if 'Design_Tools' in parts:
            return 'Design_Tools'
        elif 'IP_Cores' in parts:
            return 'IP_Cores'
        elif 'SoC_Embedded' in parts:
            return 'SoC_Embedded'
        elif 'Transceivers' in parts:
            return 'Transceivers'
        elif 'Datasheets' in parts:
            return 'Datasheets'
        else:
            return 'General'
    
    def index_all(self):
        """Tüm PDF'leri indexle"""
        print("\n" + "="*80)
        print("📚 VIVADO DÖKÜMAN İNDEXLEME")
        print("="*80)
        
        # PDF'leri bul
        pdf_files = list(self.docs_dir.rglob("*.pdf"))
        
        if not pdf_files:
            print(f"❌ {self.docs_dir} klasöründe PDF bulunamadı!")
            return
        
        print(f"\n📁 {len(pdf_files)} PDF dosyası bulundu")
        
        # Her PDF'i işle
        total_chunks = 0
        successful = 0
        
        for pdf_path in pdf_files:
            chunks = self.process_pdf(pdf_path)
            if chunks > 0:
                successful += 1
                total_chunks += chunks
        
        print("\n" + "="*80)
        print("📊 İNDEXLEME TAMAMLANDI")
        print("="*80)
        print(f"✅ Başarılı: {successful}/{len(pdf_files)} PDF")
        print(f"📝 Toplam chunk: {total_chunks}")
        print(f"💾 Database: {self.db_path}")
        print(f"📚 Collection: {self.collection.name} ({self.collection.count()} döküman)")
        print("="*80 + "\n")
    
    def test_search(self, query="AXI4-Lite interface"):
        """Arama testi"""
        print(f"\n🔍 Test Sorgusu: '{query}'")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=3
        )
        
        print("\n📄 Sonuçlar:")
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            print(f"\n{i+1}. {metadata['source']} - Sayfa {metadata['page']}")
            print(f"   {doc[:200]}...")

def main():
    """Ana program"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vivado dökümanlarını indexle")
    parser.add_argument('--docs-dir', default='../official_docs', 
                       help='Döküman klasörü')
    parser.add_argument('--db-path', default='./vivado_vectordb',
                       help='ChromaDB path')
    parser.add_argument('--reindex', action='store_true',
                       help='Collection silip yeniden indexle')
    parser.add_argument('--test', action='store_true',
                       help='İndexleme sonrası test yap')
    
    args = parser.parse_args()
    
    # Indexer oluştur
    indexer = VivadoDocsIndexer(args.docs_dir, args.db_path)
    
    # Reindex ise mevcut collection'ı sil
    if args.reindex:
        try:
            indexer.chroma_client.delete_collection("vivado_docs")
            print("🗑️ Mevcut collection silindi")
            indexer.collection = indexer.chroma_client.create_collection(
                name="vivado_docs",
                embedding_function=indexer.embedding_function
            )
        except:
            pass
    
    # İndexle
    indexer.index_all()
    
    # Test
    if args.test:
        indexer.test_search("How to create AXI4-Lite master interface?")
        indexer.test_search("Zynq PS-PL communication")
        indexer.test_search("FIFO generator IP configuration")

if __name__ == "__main__":
    main()
