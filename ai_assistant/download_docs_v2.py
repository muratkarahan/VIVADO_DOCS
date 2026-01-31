"""
AMD/Xilinx IP Core PDF Dokümanları İndirme Scripti v2
Güncellenmiş URL'ler ile çalışır (docs.amd.com)
"""

import urllib.request
import os
from pathlib import Path
import time
import ssl

# SSL sertifika kontrolünü devre dışı bırak (bazı kurumsal ağlar için)
ssl._create_default_https_context = ssl._create_unverified_context

# İndirme dizini
DOCS_DIR = Path(r"C:\Users\murat\Documents\GitHub\VIVADO_DOCS\official_docs\IP_Cores")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# AMD docs.amd.com'dan direkt PDF linkleri
# Not: AMD artık PDF'leri docs.amd.com üzerinden sunuyor
DIRECT_PDF_LINKS = [
    # === AXI Infrastructure ===
    ("pg021-axi-dma.pdf", "https://docs.amd.com/v/u/en-US/pg021_axi_dma", "AXI DMA"),
    ("pg035-axi-cdma.pdf", "https://docs.amd.com/v/u/en-US/pg034-axi-cdma", "AXI CDMA"),
    ("pg059-axi-interconnect.pdf", "https://docs.amd.com/v/u/en-US/pg059-axi-interconnect", "AXI Interconnect"),
    ("pg247-smartconnect.pdf", "https://docs.amd.com/v/u/en-US/pg247-smartconnect", "SmartConnect"),
    ("pg290-axi-noc.pdf", "https://docs.amd.com/v/u/en-US/pg313-network-on-chip", "AXI NoC"),
    
    # === Memory ===
    ("pg150-ultrascale-memory.pdf", "https://docs.amd.com/v/u/en-US/pg150-ultrascale-memory-ip", "UltraScale Memory"),
    ("pg313-axi-noc.pdf", "https://docs.amd.com/v/u/en-US/pg313-network-on-chip", "Network on Chip"),
    
    # === Ethernet ===
    ("pg157-axi-ethernet.pdf", "https://docs.amd.com/v/u/en-US/pg157-axi-ethernet", "AXI Ethernet"),
    ("pg211-xxv-ethernet.pdf", "https://docs.amd.com/v/u/en-US/pg211-xxv-ethernet", "XXV Ethernet"),
    ("pg203-cmac.pdf", "https://docs.amd.com/v/u/en-US/pg203-cmac-usplus", "CMAC"),
    
    # === PCIe ===
    ("pg194-pcie4.pdf", "https://docs.amd.com/v/u/en-US/pg194-pcie4-uscale-plus", "PCIe 4.0"),
    ("pg239-pcie-qdma.pdf", "https://docs.amd.com/v/u/en-US/pg302-pcie-qdma-versal", "PCIe QDMA"),
    
    # === High-Speed Serial ===
    ("pg168-aurora-64b66b.pdf", "https://docs.amd.com/v/u/en-US/pg168-aurora-64b66b", "Aurora 64B/66B"),
    ("pg046-aurora-8b10b.pdf", "https://docs.amd.com/v/u/en-US/pg046-aurora-8b10b", "Aurora 8B/10B"),
    ("pg182-gty.pdf", "https://docs.amd.com/v/u/en-US/pg182-gty-transceivers", "GTY Transceivers"),
    
    # === Video ===
    ("pg232-v-proc-ss.pdf", "https://docs.amd.com/v/u/en-US/pg232-v-proc-ss", "Video Processing"),
    ("pg199-vcu.pdf", "https://docs.amd.com/v/u/en-US/pg199-vcu", "Video Codec Unit"),
    
    # === DSP ===
    ("pg141-dds-compiler.pdf", "https://docs.amd.com/v/u/en-US/pg141-dds-compiler", "DDS Compiler"),
    ("pg149-xfft.pdf", "https://docs.amd.com/v/u/en-US/pg149-xfft", "FFT"),
    ("pg060-fir-compiler.pdf", "https://docs.amd.com/v/u/en-US/pg060-fir-compiler", "FIR Compiler"),
    
    # === Processor ===
    ("pg201-versal-cips.pdf", "https://docs.amd.com/v/u/en-US/pg201-versal-cips", "Versal CIPS"),
    ("pg082-processing-system7.pdf", "https://docs.amd.com/v/u/en-US/pg082-processing-system7", "Zynq PS"),
    
    # === Clock ===
    ("pg065-clk-wiz.pdf", "https://docs.amd.com/v/u/en-US/pg065-clk-wiz", "Clocking Wizard"),
    
    # === Debug ===
    ("pg172-ila.pdf", "https://docs.amd.com/v/u/en-US/pg172-ila", "ILA"),
    ("pg159-vio.pdf", "https://docs.amd.com/v/u/en-US/pg159-vio", "VIO"),
    
    # === GPIO & Peripherals ===
    ("pg144-axi-gpio.pdf", "https://docs.amd.com/v/u/en-US/pg144-axi-gpio", "AXI GPIO"),
    ("pg142-axi-uartlite.pdf", "https://docs.amd.com/v/u/en-US/pg142-axi-uartlite", "AXI UART Lite"),
    ("pg090-axi-iic.pdf", "https://docs.amd.com/v/u/en-US/pg090-axi-iic", "AXI IIC"),
    ("pg153-axi-quad-spi.pdf", "https://docs.amd.com/v/u/en-US/pg153-axi-quad-spi", "AXI Quad SPI"),
]

# Eski Xilinx support sitesinden çalışan linkler
WORKING_XILINX_LINKS = [
    # Bu linkler hala çalışıyor
    ("am011-versal-acap-trm.pdf", "https://docs.xilinx.com/viewer/book-attachment/1fxMvkBTtqJSMzgw0eCMlg/KdJPmFCR3JLwrAxVMIBrCg", "Versal TRM"),
    ("am012-versal-gt.pdf", "https://docs.xilinx.com/viewer/book-attachment/~a9A6LGM0GthPpWqRIQ7Ig/W0iXWJ7H8dNXqfPmgM5NsQ", "Versal GT"),
]

def download_pdf(item, timeout=120):
    """PDF dosyasını indir"""
    filename, url, description = item
    filepath = DOCS_DIR / filename
    
    if filepath.exists():
        size_kb = filepath.stat().st_size / 1024
        if size_kb > 50:  # En az 50 KB olmalı (gerçek PDF)
            print(f"✓ Zaten var: {filename} ({size_kb:.1f} KB) - {description}")
            return True, filename
    
    try:
        print(f"⬇ İndiriliyor: {filename} - {description}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/pdf,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://docs.amd.com/',
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            
        # PDF kontrolü
        if content.startswith(b'%PDF'):
            with open(filepath, 'wb') as f:
                f.write(content)
            size_kb = len(content) / 1024
            print(f"✓ İndirildi: {filename} ({size_kb:.1f} KB)")
            return True, filename
        else:
            # HTML olabilir, kaydet ve analiz et
            content_preview = content[:500].decode('utf-8', errors='ignore')
            if '<html' in content_preview.lower() or '<!doctype' in content_preview.lower():
                print(f"⚠ HTML döndü: {filename}")
            else:
                print(f"⚠ Bilinmeyen format: {filename}")
            return False, filename
        
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {filename}")
        return False, filename
    except Exception as e:
        print(f"✗ Hata: {filename} - {str(e)[:50]}")
        return False, filename

def try_alternative_sources():
    """Alternatif kaynaklardan indir"""
    print("\n" + "="*70)
    print("Alternatif Kaynaklar Deneniyor")
    print("="*70)
    
    # GitHub üzerindeki Xilinx açık kaynak repolarından
    GITHUB_SOURCES = [
        # Xilinx embeddedsw reposundan
        ("embeddedsw-doc.txt", "https://raw.githubusercontent.com/Xilinx/embeddedsw/master/README.md", "Embedded SW"),
    ]
    
    success = 0
    for item in GITHUB_SOURCES:
        result, _ = download_pdf(item)
        if result:
            success += 1
        time.sleep(0.5)
    
    return success

def main():
    print("="*70)
    print("AMD/Xilinx IP Core Dökümanları İndirme v2")
    print("="*70)
    print(f"Hedef dizin: {DOCS_DIR}")
    print(f"Toplam doküman: {len(DIRECT_PDF_LINKS) + len(WORKING_XILINX_LINKS)}")
    print("="*70 + "\n")
    
    success_count = 0
    fail_count = 0
    
    # Ana linklerden indir
    print("\n📂 docs.amd.com Linkleri:\n")
    for i, item in enumerate(DIRECT_PDF_LINKS, 1):
        print(f"[{i}/{len(DIRECT_PDF_LINKS)}] ", end="")
        result, _ = download_pdf(item)
        if result:
            success_count += 1
        else:
            fail_count += 1
        time.sleep(1)  # Rate limiting
    
    # Eski Xilinx linkleri
    print("\n📂 Eski Xilinx Linkleri:\n")
    for i, item in enumerate(WORKING_XILINX_LINKS, 1):
        print(f"[{i}/{len(WORKING_XILINX_LINKS)}] ", end="")
        result, _ = download_pdf(item)
        if result:
            success_count += 1
        else:
            fail_count += 1
        time.sleep(1)
    
    # Özet
    print("\n" + "="*70)
    print("İNDİRME TAMAMLANDI")
    print("="*70)
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {fail_count}")
    
    # Mevcut dosyaları listele
    existing_pdfs = list(DOCS_DIR.glob("*.pdf"))
    total_size = sum(f.stat().st_size for f in existing_pdfs) / (1024*1024)
    print(f"\n📁 Klasördeki toplam PDF: {len(existing_pdfs)}")
    print(f"💾 Toplam boyut: {total_size:.2f} MB")
    
    print("\n📋 Mevcut PDF'ler:")
    for pdf in sorted(existing_pdfs):
        size_kb = pdf.stat().st_size / 1024
        print(f"  - {pdf.name} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
