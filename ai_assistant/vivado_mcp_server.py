"""
Vivado FPGA Expert - MCP (Model Context Protocol) Server
VS Code chat participant için backend API
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from flask import Flask, request, jsonify
from flask_cors import CORS

# ============================================================================
# BAŞLATMA
# ============================================================================

load_dotenv()
app = Flask(__name__)
CORS(app)

# OpenAI ve ChromaDB başlat
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY bulunamadı!", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=api_key)

# ChromaDB bağlantısı
db_path = Path(__file__).parent / "vivado_vectordb_full"
chroma_client = chromadb.PersistentClient(
    path=str(db_path),
    settings=Settings(anonymized_telemetry=False)
)

try:
    collection = chroma_client.get_collection("vivado_full_system")
    print(f"✅ RAG Collection yüklendi: {collection.count()} doküman")
except Exception as e:
    print(f"❌ ChromaDB collection yüklenemedi: {e}", file=sys.stderr)
    sys.exit(1)

# ============================================================================
# YARDIMCI FONKSİYONLAR
# ============================================================================

def search_rag(query: str, n_results: int = 5) -> list:
    """RAG sisteminden ilgili dökümanları ara"""
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        contexts = []
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            
            contexts.append({
                'content': doc,
                'source': metadata.get('source', 'unknown'),
                'file': metadata.get('file', 'unknown'),
                'relevance': 1.0 - distance
            })
        
        return contexts
    except Exception as e:
        print(f"❌ RAG arama hatası: {e}", file=sys.stderr)
        return []

def create_prompt(query: str, contexts: list, command: str = None) -> str:
    """GPT için prompt oluştur"""
    
    system_prompt = """Sen Xilinx Vivado Design Suite konusunda uzman bir FPGA mühendisisin.
    
Uzmanlık alanların:
- Vivado IP Integrator (Block Design)
- AXI4/AXI4-Lite/AXI-Stream protokolleri
- Zynq-7000 ve UltraScale+ SoC
- TCL scripting (create_bd, add IP, connect)
- Verilog, VHDL, SystemVerilog
- Vitis HLS (High-Level Synthesis)
- DDR4, PCIe, Ethernet IP'leri
- Timing constraints (XDC)
- Implementation, synthesis

Yanıtlarında:
✅ Net ve pratik bilgi ver
✅ Kod örnekleri ekle (Verilog/VHDL/TCL)
✅ UG/PG referansları göster
✅ Best practice'leri belirt
❌ Gereksiz detaya girme
❌ Sadece teori anlatma"""

    # Context'leri formatla
    context_text = "\n\n".join([
        f"📄 **Kaynak:** {ctx['file']}\n```\n{ctx['content'][:500]}...\n```"
        for ctx in contexts[:3]
    ])
    
    # Komuta göre prompt ayarla
    if command == 'code':
        user_prompt = f"""**Görev:** Kod örneği oluştur

**Soru:** {query}

**İlgili Dökümanlar:**
{context_text}

**Beklenen:** Çalışan kod örneği (Verilog/VHDL/TCL) + açıklama"""
    
    elif command == 'explain':
        user_prompt = f"""**Görev:** Kavramı açıkla

**Soru:** {query}

**İlgili Dökümanlar:**
{context_text}

**Beklenen:** Kısa açıklama + kullanım örneği + UG/PG referans"""
    
    elif command == 'search':
        user_prompt = f"""**Görev:** Döküman ara

**Soru:** {query}

**İlgili Dökümanlar:**
{context_text}

**Beklenen:** İlgili UG/PG'leri listele + kısa özet"""
    
    else:
        user_prompt = f"""**Soru:** {query}

**İlgili Dökümanlar:**
{context_text}

**Yanıt ver:** Soru bağlamında en uygun yanıt"""
    
    return system_prompt, user_prompt

def query_gpt(query: str, contexts: list, command: str = None) -> dict:
    """GPT'ye sor ve yanıtı al"""
    try:
        system_prompt, user_prompt = create_prompt(query, contexts, command)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        answer = response.choices[0].message.content
        
        return {
            'success': True,
            'answer': answer,
            'contexts': contexts,
            'tokens': response.usage.total_tokens
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Server sağlık kontrolü"""
    return jsonify({
        'status': 'healthy',
        'collection_size': collection.count(),
        'model': 'gpt-4'
    })

@app.route('/query', methods=['POST'])
def query_endpoint():
    """Ana sorgu endpoint'i"""
    try:
        data = request.json
        query = data.get('query', '')
        command = data.get('command', None)
        n_results = data.get('n_results', 5)
        
        if not query:
            return jsonify({'error': 'Query boş olamaz'}), 400
        
        # RAG arama
        contexts = search_rag(query, n_results)
        
        # GPT'ye sor
        result = query_gpt(query, contexts, command)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search_endpoint():
    """Sadece RAG arama (GPT'siz)"""
    try:
        data = request.json
        query = data.get('query', '')
        n_results = data.get('n_results', 10)
        
        contexts = search_rag(query, n_results)
        
        return jsonify({
            'success': True,
            'results': contexts
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats_endpoint():
    """İstatistikler"""
    try:
        # Collection metadata
        results = collection.get(include=['metadatas'])
        
        # Kaynak dağılımı
        sources = {}
        for metadata in results['metadatas']:
            source = metadata.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return jsonify({
            'total_documents': len(results['ids']),
            'sources': sources,
            'database_path': str(db_path)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 Vivado FPGA Expert - MCP Server")
    print("=" * 80)
    print(f"📚 RAG Database: {collection.count()} doküman")
    print(f"🤖 Model: GPT-4")
    print(f"🌐 Server: http://localhost:5000")
    print("=" * 80)
    print()
    print("✅ Server hazır! VS Code'dan @vivado ile kullanabilirsiniz.")
    print()
    
    # Flask server başlat
    app.run(host='127.0.0.1', port=5000, debug=False)
