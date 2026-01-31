"""
Xilinx IP Core PDF Dokümanlarını İndirme Scripti
Bu script önemli IP core'ların datasheet ve user guide'larını indirir.
"""

import urllib.request
import os
from pathlib import Path

# İndirme dizini
DOCS_DIR = Path(r"C:\Users\murat\Documents\GitHub\VIVADO_DOCS\official_docs\IP_Cores")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Önemli IP Core Dokümanları - Doğrudan PDF linkleri
# Format: (dosya_adı, URL)
# Not: AMD/Xilinx bazı dökümanları archive.org veya başka kaynaklardan indirmek gerekebilir
IP_DOCS = [
    # AXI IP Cores - Xilinx.com arşivinden
    ("pg099-axi-dma.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_dma/v7_1/pg099-axi-dma.pdf"),
    ("pg034-axi-datamover.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_datamover/v5_1/pg034-axi-datamover.pdf"),
    ("pg036-axi-bram-ctrl.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_bram_ctrl/v4_1/pg036-axi-bram-ctrl.pdf"),
    ("pg059-axi-crossbar.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_crossbar/v2_1/pg059-axi-crossbar.pdf"),
    
    # Memory IP Cores
    ("pg150-ultrascale-memory-ip.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/ultrascale_memory_ip/v1_4/pg150-ultrascale-memory-ip.pdf"),
    ("ug586-7Series-MIS.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/mig_7series/v4_2/ug586_7Series_MIS.pdf"),
    
    # Ethernet IP Cores
    ("pg157-axi-ethernet.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_ethernet/v7_2/pg157-axi-ethernet.pdf"),
    ("pg138-ten-gig-eth-mac.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/ten_gig_eth_mac/v15_1/pg138-ten-gig-eth-mac.pdf"),
    
    # PCIe IP Cores
    ("pg194-pcie4-uscale-plus.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/pcie4_uscale_plus/v1_3/pg194-pcie4-uscale-plus.pdf"),
    
    # High-Speed Serial IP
    ("pg168-aurora-64b66b.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/aurora_64b66b/v12_0/pg168-aurora-64b66b.pdf"),
    ("pg046-aurora-8b10b.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/aurora_8b10b/v11_1/pg046-aurora-8b10b.pdf"),
    
    # Video IP Cores
    ("pg232-v-proc-ss.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/v_proc_ss/v2_3/pg232-v-proc-ss.pdf"),
    
    # DSP IP Cores
    ("pg141-dds-compiler.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/dds_compiler/v6_0/pg141-dds-compiler.pdf"),
    ("pg149-fft.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/xfft/v9_1/pg149-xfft.pdf"),
    ("pg060-fir-compiler.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/fir_compiler/v7_2/pg060-fir-compiler.pdf"),
    
    # Clocking
    ("pg065-clk-wiz.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/clocking_wizard/v6_0/pg065-clk-wiz.pdf"),
    
    # Processor IP
    ("ug1085-zynq-ultrascale-trm.pdf", "https://www.xilinx.com/support/documentation/user_guides/ug1085-zynq-ultrascale-trm.pdf"),
]

def download_pdf(filename, url):
    """PDF dosyasını indir"""
    filepath = DOCS_DIR / filename
    
    if filepath.exists():
        print(f"✓ Zaten var: {filename}")
        return True
    
    try:
        print(f"İndiriliyor: {filename}")
        print(f"  URL: {url}")
        
        # User-Agent header ekle (bazı siteler bunu gerektirir)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            
        with open(filepath, 'wb') as f:
            f.write(content)
            
        print(f"✓ İndirildi: {filename} ({len(content)} bytes)")
        return True
        
    except Exception as e:
        print(f"✗ Hata: {filename} - {str(e)}")
        return False

def main():
    print(f"IP Core PDF Dokümanları İndiriliyor...")
    print(f"Hedef dizin: {DOCS_DIR}")
    print(f"Toplam doküman: {len(IP_DOCS)}\n")
    
    success_count = 0
    fail_count = 0
    
    for filename, url in IP_DOCS:
        if download_pdf(filename, url):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    print("\n" + "="*60)
    print(f"İndirme tamamlandı!")
    print(f"Başarılı: {success_count}")
    print(f"Başarısız: {fail_count}")
    print(f"Toplam: {len(IP_DOCS)}")
    print("="*60)
    
    # İndirilen dosyaları listele
    downloaded_files = list(DOCS_DIR.glob("*.pdf"))
    print(f"\nİndirilen PDF'ler ({len(downloaded_files)} adet):")
    for pdf in sorted(downloaded_files):
        size_kb = pdf.stat().st_size / 1024
        print(f"  - {pdf.name} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
