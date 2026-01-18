"""
RAG Veritabanındaki tüm dökümanları listele
"""
import chromadb
from collections import defaultdict

# ChromaDB bağlan
client = chromadb.PersistentClient(path='./vivado_vectordb_full')
collection = client.get_collection('vivado_full_system')

print("=" * 80)
print("🗂️  RAG VERİTABANI DÖKÜMANLARI")
print("=" * 80)

# Tüm metadata'yı al
all_data = collection.get(include=['metadatas'])
total = len(all_data['ids'])

print(f"\n📊 Toplam Döküman: {collection.count()}")
print(f"📊 Toplam Chunk: {total}")

# Dosya tiplerini say
types = defaultdict(int)
sources = defaultdict(int)
files = defaultdict(set)

for metadata in all_data['metadatas']:
    file_type = metadata.get('type', 'unknown')
    source = metadata.get('source', 'unknown')
    filename = metadata.get('filename', 'unknown')
    
    types[file_type] += 1
    sources[source] += 1
    files[source].add(filename)

print("\n" + "=" * 80)
print("📁 DOSYA TİPLERİ")
print("=" * 80)
for ftype, count in sorted(types.items()):
    print(f"  {ftype:20s}: {count:5d} chunk")

print("\n" + "=" * 80)
print("📂 KAYNAKLAR VE DOSYA SAYILARI")
print("=" * 80)
for source in sorted(sources.keys()):
    chunk_count = sources[source]
    file_count = len(files[source])
    print(f"\n🔹 {source}")
    print(f"   Chunk: {chunk_count}, Dosya: {file_count}")
    
    # İlk 10 dosyayı göster
    if file_count <= 10:
        for f in sorted(files[source]):
            print(f"   • {f}")
    else:
        for f in sorted(list(files[source]))[:10]:
            print(f"   • {f}")
        print(f"   ... ve {file_count - 10} dosya daha")

print("\n" + "=" * 80)
print("✅ TOPLAM ÖZET")
print("=" * 80)
print(f"Kaynak Sayısı: {len(sources)}")
print(f"Benzersiz Dosya: {sum(len(f) for f in files.values())}")
print(f"Toplam Chunk: {total}")
print("=" * 80)
