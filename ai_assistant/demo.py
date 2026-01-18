"""
Demo script for testing Vivado RAG system
"""

import os
from dotenv import load_dotenv

def test_semantic_search():
    """Test ChromaDB semantic search"""
    print("\n" + "="*80)
    print("🔍 TEST 1: Semantic Search")
    print("="*80)
    
    try:
        import chromadb
        
        client = chromadb.PersistentClient(path="./vivado_vectordb")
        collection = client.get_collection(name="vivado_docs")
        
        query = "How to configure AXI4-Lite interface in IP Integrator?"
        print(f"\nQuery: {query}")
        
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        
        print("\n📄 Top 3 Results:")
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            print(f"\n{i+1}. {metadata['source']} - Page {metadata['page']}")
            print(f"   {doc[:200]}...")
        
        print("\n✅ Semantic search working!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 ChromaDB yok mu? Önce dökümanları indexleyin:")
        print("   python setup_vivado_ai.py")

def test_rag_agent():
    """Test RAG agent"""
    print("\n" + "="*80)
    print("🤖 TEST 2: RAG Agent")
    print("="*80)
    
    try:
        from vivado_agent import VivadoExpertAgent
        
        agent = VivadoExpertAgent()
        
        test_questions = [
            "AXI4-Lite nedir?",
            "Zynq PS-PL communication nasıl yapılır?",
            "FIFO generator IP nasıl kullanılır?"
        ]
        
        print("\nTest soruları:")
        for q in test_questions:
            print(f"  - {q}")
        
        print("\nİlk soruyu test ediyoruz...")
        response = agent.chat(test_questions[0])
        
        print("\n✅ RAG agent çalışıyor!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 OpenAI API key var mı?")
        print("   Set OPENAI_API_KEY environment variable")

def test_code_generation():
    """Test kod üretimi"""
    print("\n" + "="*80)
    print("💻 TEST 3: Code Generation")
    print("="*80)
    
    code_requests = [
        "AXI4-Lite slave interface Verilog",
        "Zynq GPIO driver C code",
        "Vivado TCL build script"
    ]
    
    print("\nKod örnekleri:")
    for req in code_requests:
        print(f"  ✅ {req}")
    
    print("\n💡 Gerçek kod üretimi için agent.chat() kullanın")

def main():
    """Ana demo menüsü"""
    print("\n" + "="*80)
    print("🚀 VIVADO FPGA EXPERT - Demo & Test")
    print("="*80)
    print("\nSeçenekler:")
    print("1. Semantic Search Test")
    print("2. RAG Agent Test")
    print("3. Code Generation Test")
    print("4. Tüm testleri çalıştır")
    print("5. Çıkış")
    
    choice = input("\nSeçiminiz (1-5): ").strip()
    
    if choice == '1':
        test_semantic_search()
    elif choice == '2':
        test_rag_agent()
    elif choice == '3':
        test_code_generation()
    elif choice == '4':
        test_semantic_search()
        test_rag_agent()
        test_code_generation()
    else:
        print("\n👋 Çıkış yapılıyor...")

if __name__ == "__main__":
    load_dotenv()
    main()
