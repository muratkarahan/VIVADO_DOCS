"""
AMD/Xilinx IP Core PDF İndirme - Extended v5
Farklı versiyon numaraları ile deneme
"""

import os
from pathlib import Path
import time
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

DOCS_DIR = Path(r"C:\Users\murat\Documents\GitHub\VIVADO_DOCS\official_docs\IP_Cores")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Çeşitli versiyon numaralarıyla deneme listesi
# (dosya_adı, base_url_template, ip_name, versiyon_listesi)
IP_DOCS_TO_TRY = [
    # Block Memory Gen - v8_3, v8_4, v8_5 dene
    {
        "filename": "pg058-blk-mem-gen.pdf",
        "name": "Block Memory Generator",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/blk_mem_gen",
        "versions": ["v8_5", "v8_4", "v8_3", "v8_2"]
    },
    # FIFO Generator
    {
        "filename": "pg057-fifo-generator.pdf", 
        "name": "FIFO Generator",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/fifo_generator",
        "versions": ["v13_3", "v13_2", "v13_1", "v13_0"]
    },
    # Clocking Wizard
    {
        "filename": "pg065-clk-wiz.pdf",
        "name": "Clocking Wizard",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/clk_wiz",
        "versions": ["v6_1", "v6_0", "v5_4", "v5_3"]
    },
    # Processor System Reset
    {
        "filename": "pg064-proc-sys-reset.pdf",
        "name": "Processor System Reset",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/proc_sys_reset",
        "versions": ["v5_1", "v5_0", "v4_0"]
    },
    # ILA
    {
        "filename": "pg172-ila.pdf",
        "name": "ILA",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/ila",
        "versions": ["v6_3", "v6_2", "v6_1", "v6_0"]
    },
    # AXI Timer
    {
        "filename": "pg078-axi-timer.pdf",
        "name": "AXI Timer",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_timer",
        "versions": ["v2_1", "v2_0", "v1_03_a"]
    },
    # AXI Interrupt Controller
    {
        "filename": "pg079-axi-intc.pdf",
        "name": "AXI Interrupt Controller",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_intc",
        "versions": ["v4_2", "v4_1", "v4_0"]
    },
    # Processing System 7 (Zynq)
    {
        "filename": "pg082-processing-system7.pdf",
        "name": "Zynq Processing System",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/processing_system7",
        "versions": ["v5_6", "v5_5", "v5_4"]
    },
    # AXI BRAM Controller
    {
        "filename": "pg036-axi-bram-ctrl.pdf",
        "name": "AXI BRAM Controller",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_bram_ctrl",
        "versions": ["v4_2", "v4_1", "v4_0"]
    },
    # AXI Crossbar
    {
        "filename": "pg059-axi-crossbar.pdf",
        "name": "AXI Crossbar",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_crossbar",
        "versions": ["v2_2", "v2_1", "v2_0"]
    },
    # AXI Data Mover
    {
        "filename": "pg034-axi-datamover.pdf",
        "name": "AXI DataMover",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_datamover",
        "versions": ["v5_2", "v5_1", "v5_0"]
    },
    # AXI FIFO MM S
    {
        "filename": "pg085-axi-fifo-mm-s.pdf",
        "name": "AXI Stream FIFO",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_fifo_mm_s",
        "versions": ["v4_3", "v4_2", "v4_1"]
    },
    # MIG 7 Series
    {
        "filename": "ug586-7series-mis.pdf",
        "name": "7 Series MIG",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/mig_7series",
        "versions": ["v4_3", "v4_2", "v4_1", "v4_0"]
    },
    # UltraScale Memory
    {
        "filename": "pg150-ultrascale-memory-ip.pdf",
        "name": "UltraScale Memory IP",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/ultrascale_memory_ip",
        "versions": ["v1_5", "v1_4", "v1_3"]
    },
    # FIR Compiler
    {
        "filename": "pg060-fir-compiler.pdf",
        "name": "FIR Compiler",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/fir_compiler",
        "versions": ["v7_3", "v7_2", "v7_1"]
    },
    # DDS Compiler
    {
        "filename": "pg141-dds-compiler.pdf",
        "name": "DDS Compiler",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/dds_compiler",
        "versions": ["v6_1", "v6_0", "v5_0"]
    },
    # FFT
    {
        "filename": "pg149-xfft.pdf",
        "name": "FFT",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/xfft",
        "versions": ["v9_2", "v9_1", "v9_0"]
    },
    # Aurora 8B10B
    {
        "filename": "pg046-aurora-8b10b.pdf",
        "name": "Aurora 8B/10B",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/aurora_8b10b",
        "versions": ["v11_2", "v11_1", "v11_0"]
    },
    # Aurora 64B66B
    {
        "filename": "pg168-aurora-64b66b.pdf",
        "name": "Aurora 64B/66B",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/aurora_64b66b",
        "versions": ["v12_1", "v12_0", "v11_2"]
    },
    # AXI Ethernet
    {
        "filename": "pg157-axi-ethernet.pdf",
        "name": "AXI Ethernet",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_ethernet",
        "versions": ["v7_3", "v7_2", "v7_1"]
    },
    # 10G Ethernet MAC
    {
        "filename": "pg138-ten-gig-eth-mac.pdf",
        "name": "10G Ethernet MAC",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/ten_gig_eth_mac",
        "versions": ["v15_2", "v15_1", "v15_0"]
    },
    # AXI PCIe
    {
        "filename": "pg054-axi-pcie.pdf",
        "name": "AXI PCIe Bridge",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_pcie",
        "versions": ["v2_10", "v2_9", "v2_8"]
    },
    # PCIe 4.0 UltraScale+
    {
        "filename": "pg194-pcie4-uscale-plus.pdf",
        "name": "PCIe 4.0 UltraScale+",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/pcie4_uscale_plus",
        "versions": ["v1_4", "v1_3", "v1_2"]
    },
    # Video Proc SS
    {
        "filename": "pg232-v-proc-ss.pdf",
        "name": "Video Processing Subsystem",
        "base": "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/v_proc_ss",
        "versions": ["v2_4", "v2_3", "v2_2"]
    },
]

def try_download_with_versions(doc_info, timeout=60):
    """Farklı versiyonlarla PDF indirmeyi dene"""
    filename = doc_info["filename"]
    name = doc_info["name"]
    base_url = doc_info["base"]
    versions = doc_info["versions"]
    
    filepath = DOCS_DIR / filename
    
    if filepath.exists():
        size_kb = filepath.stat().st_size / 1024
        if size_kb > 300:
            print(f"✓ Mevcut: {filename} ({size_kb:.1f} KB)")
            return True
    
    for version in versions:
        url = f"{base_url}/{version}/{filename}"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/pdf,*/*',
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read()
                
            if content.startswith(b'%PDF'):
                size_kb = len(content) / 1024
                if size_kb > 100:
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"✓ İndirildi ({version}): {filename} ({size_kb:.1f} KB)")
                    return True
        except:
            continue
    
    print(f"✗ Bulunamadı: {filename} - {name}")
    return False

def main():
    print("="*70)
    print("AMD/Xilinx IP Core PDF İndirme - Extended v5")
    print("Farklı versiyonlar deneniyor...")
    print("="*70)
    print(f"Hedef: {DOCS_DIR}")
    print(f"Toplam IP: {len(IP_DOCS_TO_TRY)}")
    print("="*70 + "\n")
    
    success = 0
    failed = 0
    
    for i, doc_info in enumerate(IP_DOCS_TO_TRY, 1):
        print(f"[{i}/{len(IP_DOCS_TO_TRY)}] ", end="")
        if try_download_with_versions(doc_info):
            success += 1
        else:
            failed += 1
        time.sleep(0.3)
    
    print("\n" + "="*70)
    print("SONUÇ")
    print("="*70)
    print(f"✅ Başarılı: {success}")
    print(f"❌ Başarısız: {failed}")
    
    pdfs = list(DOCS_DIR.glob("*.pdf"))
    total_size = sum(f.stat().st_size for f in pdfs) / (1024*1024)
    print(f"\n📁 Toplam PDF: {len(pdfs)}")
    print(f"💾 Toplam boyut: {total_size:.2f} MB")

if __name__ == "__main__":
    main()
