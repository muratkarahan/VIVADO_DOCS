"""
AMD/Xilinx IP Core PDF İndirme - v4 Final
Çalışan CDN linkleri ile
"""

import os
from pathlib import Path
import time
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

DOCS_DIR = Path(r"C:\Users\murat\Documents\GitHub\VIVADO_DOCS\official_docs\IP_Cores")
DESIGN_TOOLS_DIR = Path(r"C:\Users\murat\Documents\GitHub\VIVADO_DOCS\official_docs\Design_Tools")
DOCS_DIR.mkdir(parents=True, exist_ok=True)
DESIGN_TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# Xilinx CDN'den çalışan linkler (IP Dokümantasyonu)
# Format: (dosya_adı, URL, açıklama, hedef_dizin)
VERIFIED_DOCS = [
    # === AXI IP Cores (2020+ versiyonlar) ===
    ("pg021-axi-dma.pdf", 
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_dma/v7_1/pg021_axi_dma.pdf",
     "AXI DMA v7.1", DOCS_DIR),
    
    ("pg034-axi-cdma.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_cdma/v4_1/pg034-axi-cdma.pdf",
     "AXI CDMA v4.1", DOCS_DIR),
     
    ("pg142-axi-uartlite.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_uartlite/v2_0/pg142-axi-uartlite.pdf",
     "AXI UART Lite v2.0", DOCS_DIR),
     
    ("pg143-axi-uart16550.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_uart16550/v2_0/pg143-axi-uart16550.pdf",
     "AXI UART 16550 v2.0", DOCS_DIR),
     
    ("pg144-axi-gpio.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_gpio/v2_0/pg144-axi-gpio.pdf",
     "AXI GPIO v2.0", DOCS_DIR),
     
    ("pg153-axi-quad-spi.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_quad_spi/v3_2/pg153-axi-quad-spi.pdf",
     "AXI Quad SPI v3.2", DOCS_DIR),
     
    ("pg159-vio.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/vio/v3_0/pg159-vio.pdf",
     "VIO v3.0", DOCS_DIR),
     
    ("pg247-smartconnect.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/smartconnect/v1_0/pg247-smartconnect.pdf",
     "SmartConnect v1.0", DOCS_DIR),
     
    # Ek IP Dokümanları 
    ("pg078-axi-timer.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_timer/v2_0/pg078-axi-timer.pdf",
     "AXI Timer v2.0", DOCS_DIR),
    
    ("pg079-axi-intc.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_intc/v4_1/pg079-axi-intc.pdf",
     "AXI Interrupt Controller v4.1", DOCS_DIR),
    
    ("pg082-processing-system7.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/processing_system7/v5_5/pg082-processing-system7.pdf",
     "Zynq-7000 PS v5.5", DOCS_DIR),
     
    ("pg090-axi-iic.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_iic/v2_0/pg090-axi-iic.pdf",
     "AXI IIC v2.0", DOCS_DIR),
     
    ("pg064-proc-sys-reset.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/proc_sys_reset/v5_0/pg064-proc-sys-reset.pdf",
     "Processor System Reset v5.0", DOCS_DIR),
    
    ("pg057-fifo-generator.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/fifo_generator/v13_2/pg057-fifo-generator.pdf",
     "FIFO Generator v13.2", DOCS_DIR),
    
    ("pg058-blk-mem-gen.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/blk_mem_gen/v8_4/pg058-blk-mem-gen.pdf",
     "Block Memory Generator v8.4", DOCS_DIR),
     
    ("pg065-clk-wiz.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/clk_wiz/v6_0/pg065-clk-wiz.pdf",
     "Clocking Wizard v6.0", DOCS_DIR),
     
    ("pg172-ila.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/ila/v6_2/pg172-ila.pdf",
     "ILA v6.2", DOCS_DIR),
]

def download_pdf(item, timeout=120):
    """PDF dosyasını indir"""
    filename, url, description, target_dir = item
    filepath = target_dir / filename
    
    if filepath.exists():
        size_kb = filepath.stat().st_size / 1024
        if size_kb > 300:  # Gerçek PDF en az 300KB olmalı
            print(f"✓ Mevcut: {filename} ({size_kb:.1f} KB)")
            return True, filename
    
    try:
        print(f"⬇ İndiriliyor: {filename} - {description}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/pdf,application/octet-stream,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            
        if content.startswith(b'%PDF'):
            size_kb = len(content) / 1024
            if size_kb > 100:  # En az 100KB PDF kabul et
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"✓ İndirildi: {filename} ({size_kb:.1f} KB)")
                return True, filename
            else:
                print(f"⚠ Çok küçük PDF: {filename} ({size_kb:.1f} KB)")
                return False, filename
        else:
            print(f"⚠ PDF değil: {filename}")
            return False, filename
        
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {filename}")
        return False, filename
    except Exception as e:
        print(f"✗ Hata: {filename} - {str(e)[:60]}")
        return False, filename

def main():
    print("="*70)
    print("AMD/Xilinx Doküman İndirme - Final v4")
    print("="*70)
    print(f"IP Cores: {DOCS_DIR}")
    print(f"Toplam: {len(VERIFIED_DOCS)} doküman")
    print("="*70 + "\n")
    
    success = 0
    failed = 0
    failed_list = []
    
    for i, item in enumerate(VERIFIED_DOCS, 1):
        print(f"[{i}/{len(VERIFIED_DOCS)}] ", end="")
        result, filename = download_pdf(item)
        if result:
            success += 1
        else:
            failed += 1
            failed_list.append(filename)
        time.sleep(0.5)
    
    print("\n" + "="*70)
    print("SONUÇ")
    print("="*70)
    print(f"✅ Başarılı: {success}")
    print(f"❌ Başarısız: {failed}")
    
    # Mevcut dosyaları listele
    pdfs = list(DOCS_DIR.glob("*.pdf"))
    total_size = sum(f.stat().st_size for f in pdfs) / (1024*1024)
    print(f"\n📁 IP_Cores içindeki PDF sayısı: {len(pdfs)}")
    print(f"💾 Toplam boyut: {total_size:.2f} MB")
    
    print("\n📋 Mevcut PDF'ler:")
    for pdf in sorted(pdfs, key=lambda x: x.stat().st_size, reverse=True):
        size_kb = pdf.stat().st_size / 1024
        print(f"  ✓ {pdf.name} ({size_kb:.1f} KB)")
    
    if failed_list:
        print(f"\n⚠ İndirilemeyenler ({len(failed_list)}):")
        for f in failed_list:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
