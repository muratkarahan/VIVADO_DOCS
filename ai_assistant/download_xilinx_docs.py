"""
AMD/Xilinx Resmi Doküman İndirme Scripti
Önemli User Guide, Product Guide ve Datasheet'leri indirir
"""
import requests
from pathlib import Path
from tqdm import tqdm
import time

# İndirme dizinleri
DOWNLOAD_DIRS = {
    'user_guides': Path('../official_docs/Design_Tools'),
    'product_guides': Path('../official_docs/IP_Cores'),
    'datasheets': Path('../official_docs/Datasheets'),
}

# Dizinleri oluştur
for dir_path in DOWNLOAD_DIRS.values():
    dir_path.mkdir(parents=True, exist_ok=True)

# AMD/Xilinx Doküman URL'leri
DOCUMENTS = {
    # ========== USER GUIDES (Design Tools) ==========
    'user_guides': {
        'UG835': {
            'name': 'Vivado Design Suite Tcl Command Reference Guide',
            'url': 'https://docs.amd.com/r/en-US/ug835-vivado-tcl-commands/Introduction'
        },
        'UG892': {
            'name': 'Vivado Design Suite User Guide - Design Flows Overview',
            'url': 'https://docs.amd.com/r/en-US/ug892-vivado-design-flows-overview/Introduction'
        },
        'UG893': {
            'name': 'Vivado Design Suite User Guide - Using the Vivado IDE',
            'url': 'https://docs.amd.com/r/en-US/ug893-vivado-ide/Introduction'
        },
        'UG894': {
            'name': 'Vivado Design Suite User Guide - Using Constraints',
            'url': 'https://docs.amd.com/r/en-US/ug894-vivado-tcl-scripting/Introduction'
        },
        'UG896': {
            'name': 'Vivado Design Suite User Guide - Getting Started',
            'url': 'https://docs.amd.com/r/en-US/ug896-vivado-ip/Introduction'
        },
        'UG901': {
            'name': 'Vivado Design Suite User Guide - Synthesis',
            'url': 'https://docs.amd.com/r/en-US/ug901-vivado-synthesis/Introduction'
        },
        'UG904': {
            'name': 'Vivado Design Suite User Guide - Implementation',
            'url': 'https://docs.amd.com/r/en-US/ug904-vivado-implementation/Introduction'
        },
        'UG906': {
            'name': 'Vivado Design Suite User Guide - Design Analysis and Closure',
            'url': 'https://docs.amd.com/r/en-US/ug906-vivado-design-analysis/Introduction'
        },
    },
    
    # ========== PRODUCT GUIDES (IP Cores) ==========
    'product_guides': {
        'PG021': {
            'name': 'AXI DMA Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg021_axi_dma/Introduction'
        },
        'PG144': {
            'name': 'AXI GPIO Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg144-axi-gpio/Introduction'
        },
        'PG142': {
            'name': 'AXI UART Lite Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg142-axi-uartlite/Introduction'
        },
        'PG090': {
            'name': 'AXI IIC Bus Interface Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg090-axi-iic/Introduction'
        },
        'PG065': {
            'name': 'Clocking Wizard Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg065-clk-wiz/Introduction'
        },
        'PG058': {
            'name': 'Block Memory Generator Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg058-blk-mem-gen/Introduction'
        },
        'PG157': {
            'name': 'AXI Interconnect Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg157-axi-interconnect/Introduction'
        },
        'PG247': {
            'name': 'SmartConnect Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg247-smartconnect/Introduction'
        },
        'PG117': {
            'name': 'FIFO Generator Product Guide',
            'url': 'https://docs.amd.com/r/en-US/pg057-fifo-generator/Introduction'
        },
    },
    
    # ========== DATASHEETS ==========
    'datasheets': {
        'DS180': {
            'name': '7 Series FPGAs Overview',
            'url': 'https://docs.amd.com/v/u/en-US/ds180_7Series_Overview'
        },
        'DS190': {
            'name': 'Zynq-7000 SoC Overview',
            'url': 'https://docs.amd.com/v/u/en-US/ds190-Zynq-7000-Overview'
        },
        'DS925': {
            'name': 'UltraScale Architecture and Product Data Sheet - Overview',
            'url': 'https://docs.amd.com/v/u/en-US/ds925-zynq-ultrascale-plus'
        },
    },
}

# GitHub Xilinx Example Designs
GITHUB_EXAMPLES = {
    'tcl_store': {
        'name': 'Xilinx Tcl Store (Utility Scripts)',
        'url': 'https://github.com/Xilinx/XilinxTclStore/archive/refs/heads/master.zip',
    },
    'design_tutorials': {
        'name': 'Vivado Design Tutorials',
        'url': 'https://github.com/Xilinx/Vivado-Design-Tutorials/archive/refs/heads/master.zip',
    },
    'hdl_examples': {
        'name': 'Xilinx HDL Examples',
        'url': 'https://github.com/Xilinx/Vivado-Design-Tutorials/archive/refs/heads/master.zip',
    },
}

def download_file(url, dest_path, desc="Downloading"):
    """Dosya indir (progress bar ile)"""
    try:
        print(f"\n📥 {desc}...")
        print(f"   URL: {url}")
        print(f"   Hedef: {dest_path}")
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"   {desc}") as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        print(f"   ✅ Başarıyla indirildi!")
        return True
    except Exception as e:
        print(f"   ❌ Hata: {e}")
        return False

def main():
    print("=" * 100)
    print("📥 AMD/XILINX RESMI DOKÜMANLARI İNDİRME ARACI")
    print("=" * 100)
    
    print("\n⚠️  NOT: AMD docs.amd.com sitesi PDF doğrudan indirme sunmuyor.")
    print("Bu dokümanlar web sayfası olarak mevcut. Manuel indirme için URL'ler listeleniyor.\n")
    
    total_docs = sum(len(docs) for docs in DOCUMENTS.values())
    
    # URL listesini dosyaya kaydet
    urls_file = Path('../official_docs/DOWNLOAD_LINKS.md')
    
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write("# AMD/Xilinx Resmi Dokümanlar - İndirme Linkleri\n\n")
        f.write("Bu dokümanlar AMD/Xilinx'in resmi docs.amd.com sitesinde bulunur.\n")
        f.write("PDF indirmek için her sayfanın sağ üst köşesindeki **Download PDF** butonunu kullanın.\n\n")
        f.write(f"**Toplam: {total_docs} doküman**\n\n")
        f.write("---\n\n")
        
        for category, docs in DOCUMENTS.items():
            category_name = category.replace('_', ' ').title()
            dir_path = DOWNLOAD_DIRS[category]
            
            f.write(f"## {category_name}\n\n")
            f.write(f"**Hedef Klasör**: `{dir_path}`\n\n")
            
            for doc_id, info in docs.items():
                f.write(f"### {doc_id} - {info['name']}\n")
                f.write(f"- **URL**: {info['url']}\n")
                f.write(f"- **İndirme**: Sayfayı açın → Sağ üstten 'Download PDF' → `{dir_path}/{doc_id}.pdf`\n\n")
        
        # GitHub Examples
        f.write("---\n\n## GitHub Örnek Kodları (Otomatik İndirilebilir)\n\n")
        for repo_id, info in GITHUB_EXAMPLES.items():
            f.write(f"### {info['name']}\n")
            f.write(f"- **URL**: {info['url']}\n")
            f.write(f"- **Kullanım**: Bu script ile otomatik indirilebilir\n\n")
    
    print(f"✅ İndirme linkleri kaydedildi: {urls_file}")
    
    # Otomatik indirilebilecek kaynaklar
    print("\n" + "=" * 100)
    print("📦 OTOMATİK İNDİRİLEBİLECEK KAYNAKLAR (GitHub)")
    print("=" * 100)
    
    # Xilinx GitHub Tcl Store
    print("\n🔧 1. Xilinx Tcl Store")
    print("   Vivado için TCL utility scriptleri ve araçlar")
    tcl_store_url = GITHUB_EXAMPLES['tcl_store']['url']
    tcl_store_path = Path('../code_examples/XilinxTclStore-master.zip')
    
    download = input("\n   İndirmek ister misiniz? (y/n): ")
    if download.lower() == 'y':
        tcl_store_path.parent.mkdir(parents=True, exist_ok=True)
        download_file(tcl_store_url, tcl_store_path, desc="Xilinx Tcl Store")
    
    # Vivado Example Designs
    print("\n🔧 2. Vivado Design Tutorials")
    print("   Vivado design tutorial'ları ve örnek projeler")
    example_url = GITHUB_EXAMPLES['design_tutorials']['url']
    example_path = Path('../vivado-examples/Vivado-Design-Tutorials-master.zip')
    
    download = input("\n   İndirmek ister misiniz? (y/n): ")
    if download.lower() == 'y':
        example_path.parent.mkdir(parents=True, exist_ok=True)
        download_file(example_url, example_path, desc="Vivado Design Tutorials")
    
    print("\n" + "=" * 100)
    print("✅ İŞLEM TAMAMLANDI")
    print("=" * 100)
    
    print(f"""
📋 SONUÇ:
   • İndirme linkleri: {urls_file}
   • Manuel PDF indirme: docs.amd.com'dan 'Download PDF' ile
   • Otomatik indirilen: GitHub repoları (seçildiyse)
   
🔄 SONRAKI ADIMLAR:
   
   📖 Manuel PDF İndirme:
   1. {urls_file} dosyasını açın
   2. Her doküman için URL'i ziyaret edin
   3. Sayfanın sağ üst köşesindeki "Download PDF" butonunu tıklayın
   4. İlgili klasöre kaydedin (UG'ler → Design_Tools, PG'ler → IP_Cores, DS'ler → Datasheets)
   
   📦 İndirilen ZIP'leri Extract Etme:
   1. cd ../code_examples (veya ../vivado-examples)
   2. unzip *.zip  (veya Extract Here)
   
   🤖 RAG Sistemine Ekleme:
   1. cd ai_assistant
   2. python train_rag_full_system.py
   
   Bu dokümanlar RAG sisteminize eklenecek ve AI asistanınız
   Vivado, IP Core'lar ve FPGA tasarımı hakkında çok daha detaylı
   bilgi verebilecek!
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  İşlem iptal edildi")
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        import traceback
        traceback.print_exc()
