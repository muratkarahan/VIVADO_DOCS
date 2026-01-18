"""
Xilinx IP Core ve Vivado altındaki TÜM PDF dokümanları bul
"""
from pathlib import Path
from collections import defaultdict

print("=" * 100)
print("🔍 XILINX/VIVADO PDF DOKÜMANLARI TARANYOR...")
print("=" * 100)

# Tüm PDF'leri bul
xilinx_path = Path("C:/Xilinx/2025.1")
all_pdfs = list(xilinx_path.rglob("*.pdf"))

print(f"\n📊 Toplam PDF: {len(all_pdfs)}")

# Kategorize et
categories = {
    'IP Core Docs': [],
    'Memory Interface (MIG)': [],
    'Embedded Software': [],
    'User Guides': [],
    'Datasheets': [],
    'Other': []
}

for pdf in all_pdfs:
    path_str = str(pdf).lower()
    name = pdf.name.lower()
    
    if 'mig' in path_str or 'memory' in path_str:
        categories['Memory Interface (MIG)'].append(pdf)
    elif 'embeddedsw' in path_str:
        categories['Embedded Software'].append(pdf)
    elif 'ug' in name and name.endswith('.pdf'):  # User Guide
        categories['User Guides'].append(pdf)
    elif 'ds' in name and name.endswith('.pdf'):  # Datasheet
        categories['Datasheets'].append(pdf)
    elif 'ip' in path_str or 'doc' in path_str:
        categories['IP Core Docs'].append(pdf)
    else:
        categories['Other'].append(pdf)

# Sonuçları göster
print("\n" + "=" * 100)
print("📂 KATEGORİLERE GÖRE PDF DOKÜMANLARI")
print("=" * 100)

for cat, pdfs in categories.items():
    if pdfs:
        print(f"\n🔹 {cat} ({len(pdfs)} PDF)")
        print("-" * 100)
        
        # Benzersiz dosyaları göster (duplicate'leri çıkar)
        unique_names = {}
        for pdf in pdfs:
            if pdf.name not in unique_names:
                unique_names[pdf.name] = pdf
        
        for name, pdf in sorted(unique_names.items()):
            print(f"  • {name:50s} ({pdf.parent.name}/)")

# Detaylı liste kaydet
output_file = Path("xilinx_all_pdfs_list.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 100 + "\n")
    f.write("XILINX 2025.1 - TÜM PDF DOKÜMANLARI\n")
    f.write("=" * 100 + "\n\n")
    
    f.write(f"Toplam PDF: {len(all_pdfs)}\n\n")
    
    for cat, pdfs in categories.items():
        if pdfs:
            f.write(f"\n{'=' * 100}\n")
            f.write(f"{cat}\n")
            f.write(f"{'=' * 100}\n")
            f.write(f"Toplam: {len(pdfs)} PDF\n\n")
            
            for pdf in sorted(pdfs, key=lambda x: x.name):
                f.write(f"{pdf}\n")

print(f"\n✅ Detaylı liste kaydedildi: {output_file}")

# Özet
print("\n" + "=" * 100)
print("📊 ÖZET")
print("=" * 100)
print(f"Toplam PDF: {len(all_pdfs)}")
print(f"Benzersiz PDF: {len(set(p.name for p in all_pdfs))}")

print("\n⚠️ NOT:")
print("IP Core'ların çoğu PDF dokümanı Xilinx kurulumunda değil,")
print("online doküman portalında bulunur:")
print("  • https://docs.amd.com/")
print("  • https://www.xilinx.com/products/intellectual-property.html")

print("\n" + "=" * 100)
print("✨ TARAMA TAMAMLANDI")
print("=" * 100)
