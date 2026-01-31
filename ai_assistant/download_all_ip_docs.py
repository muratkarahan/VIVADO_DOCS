"""
Xilinx Tüm IP Core PDF Dokümanlarını İndirme Scripti
597 IP core için Product Guide (PG) ve User Guide (UG) dokümanları
"""

import urllib.request
import os
import time
from pathlib import Path
import concurrent.futures

# İndirme dizini
DOCS_DIR = Path(r"C:\Users\murat\Documents\GitHub\VIVADO_DOCS\official_docs\IP_Cores")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Tüm IP Core doküman linkleri (Xilinx.com'dan)
# Format: (dosya_adı, URL, kategori)
ALL_IP_DOCS = [
    # === AXI Infrastructure ===
    ("pg099-axi-dma.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_dma/v7_1/pg099-axi-dma.pdf", "AXI"),
    ("pg034-axi-datamover.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_datamover/v5_1/pg034-axi-datamover.pdf", "AXI"),
    ("pg036-axi-bram-ctrl.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_bram_ctrl/v4_1/pg036-axi-bram-ctrl.pdf", "AXI"),
    ("pg059-axi-crossbar.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_crossbar/v2_1/pg059-axi-crossbar.pdf", "AXI"),
    ("pg144-axi-interconnect.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_interconnect/v2_1/pg144-axi-interconnect.pdf", "AXI"),
    ("pg051-axi-protocol-converter.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_protocol_converter/v2_1/pg051-axi-protocol-converter.pdf", "AXI"),
    ("pg055-axi-clock-converter.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_clock_converter/v2_1/pg055-axi-clock-converter.pdf", "AXI"),
    ("pg056-axi-dwidth-converter.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_dwidth_converter/v2_1/pg056-axi-dwidth-converter.pdf", "AXI"),
    ("pg085-axi-fifo-mm-s.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_fifo_mm_s/v4_2/pg085-axi-fifo-mm-s.pdf", "AXI"),
    ("pg144-axi-register-slice.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_register_slice/v2_1/pg144-axi-register-slice.pdf", "AXI"),
    
    # === Memory Controllers ===
    ("pg150-ultrascale-memory-ip.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/ultrascale_memory_ip/v1_4/pg150-ultrascale-memory-ip.pdf", "Memory"),
    ("ug586-7Series-MIS.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/mig_7series/v4_2/ug586_7Series_MIS.pdf", "Memory"),
    ("pg313-network-on-chip.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_noc/v1_0/pg313-network-on-chip.pdf", "Memory"),
    
    # === Ethernet & Networking ===
    ("pg157-axi-ethernet.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_ethernet/v7_2/pg157-axi-ethernet.pdf", "Network"),
    ("pg138-ten-gig-eth-mac.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/ten_gig_eth_mac/v15_1/pg138-ten-gig-eth-mac.pdf", "Network"),
    ("pg211-xxv-ethernet.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/xxv_ethernet/v3_1/pg211-xxv-ethernet.pdf", "Network"),
    ("pg203-cmac-usplus.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/cmac_usplus/v3_1/pg203-cmac-usplus.pdf", "Network"),
    
    # === PCIe ===
    ("pg194-pcie4-uscale-plus.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/pcie4_uscale_plus/v1_3/pg194-pcie4-uscale-plus.pdf", "PCIe"),
    ("pg213-pcie-dma-versal.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/pcie_dma_versal/v2_1/pg213-pcie-dma-versal.pdf", "PCIe"),
    ("pg156-pcie-uscale.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/pcie_uscale/v4_4/pg156-pcie-uscale.pdf", "PCIe"),
    ("pg054-pcie-bridge.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_pcie/v2_9/pg054-axi-pcie.pdf", "PCIe"),
    
    # === High-Speed Serial ===
    ("pg168-aurora-64b66b.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/aurora_64b66b/v12_0/pg168-aurora-64b66b.pdf", "Serial"),
    ("pg046-aurora-8b10b.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/aurora_8b10b/v11_1/pg046-aurora-8b10b.pdf", "Serial"),
    ("pg053-jesd204.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/jesd204/v7_2/pg053-jesd204.pdf", "Serial"),
    ("pg074-gth-transceivers.pdf", "https://www.xilinx.com/support/documentation/user_guides/ug576-ultrascale-gth-transceivers.pdf", "Serial"),
    ("pg182-gty-transceivers.pdf", "https://www.xilinx.com/support/documentation/user_guides/ug578-ultrascale-gty-transceivers.pdf", "Serial"),
    
    # === Video & Imaging ===
    ("pg232-v-proc-ss.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/v_proc_ss/v2_3/pg232-v-proc-ss.pdf", "Video"),
    ("pg235-hdmi-gt-controller.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/hdmi_gt_ctrl/v1_0/pg235-hdmi-gt-controller.pdf", "Video"),
    ("pg199-vcu.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/vcu/v1_2/pg199-vcu.pdf", "Video"),
    ("pg231-v-tpg.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/v_tpg/v8_2/pg231-v-tpg.pdf", "Video"),
    
    # === DSP ===
    ("pg141-dds-compiler.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/dds_compiler/v6_0/pg141-dds-compiler.pdf", "DSP"),
    ("pg149-fft.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/xfft/v9_1/pg149-xfft.pdf", "DSP"),
    ("pg060-fir-compiler.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/fir_compiler/v7_2/pg060-fir-compiler.pdf", "DSP"),
    ("pg105-cmpy.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/cmpy/v6_0/pg105-cmpy.pdf", "DSP"),
    ("pg104-cordic.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/cordic/v6_0/pg104-cordic.pdf", "DSP"),
    ("pg111-div-gen.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/div_gen/v5_1/pg111-div-gen.pdf", "DSP"),
    
    # === Math & Logic ===
    ("pg108-c-addsub.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/c_addsub/v12_0/pg108-c-addsub.pdf", "Math"),
    ("pg109-mult-gen.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/mult_gen/v12_0/pg109-mult-gen.pdf", "Math"),
    ("pg121-floating-point.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/floating_point/v7_1/pg121-floating-point.pdf", "Math"),
    
    # === Storage & Memory ===
    ("pg022-fifo-generator.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/fifo_generator/v13_2/pg057-fifo-generator.pdf", "Storage"),
    ("pg073-blk-mem-gen.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/blk_mem_gen/v8_4/pg058-blk-mem-gen.pdf", "Storage"),
    
    # === Clocking & Reset ===
    ("pg065-clk-wiz.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/clocking_wizard/v6_0/pg065-clk-wiz.pdf", "Clock"),
    ("pg064-proc-sys-reset.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/proc_sys_reset/v5_0/pg064-proc-sys-reset.pdf", "Clock"),
    
    # === Processor & Embedded ===
    ("ug1085-zynq-ultrascale-trm.pdf", "https://www.xilinx.com/support/documentation/user_guides/ug1085-zynq-ultrascale-trm.pdf", "Processor"),
    ("pg201-versal-cips.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/versal_cips/v3_0/pg201-versal-cips.pdf", "Processor"),
    ("pg082-processing-system7.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/processing_system7/v5_5/pg082-processing-system7.pdf", "Processor"),
    ("pg164-zynq-mpsoc-ps.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/zynq_ultra_ps_e/v3_3/pg201-zynq-ultra-ps-e.pdf", "Processor"),
    
    # === System Monitoring ===
    ("pg091-system-monitor.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/system_management_wiz/v1_3/pg091-system-management-wiz.pdf", "Monitor"),
    
    # === GPIO & IO ===
    ("pg144-axi-gpio.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_gpio/v2_0/pg144-axi-gpio.pdf", "IO"),
    ("pg099-axi-quad-spi.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_quad_spi/v3_2/pg153-axi-quad-spi.pdf", "IO"),
    ("pg099-axi-iic.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_iic/v2_0/pg090-axi-iic.pdf", "IO"),
    ("pg142-axi-uart16550.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/axi_uart16550/v2_0/pg143-axi-uart16550.pdf", "IO"),
    
    # === Security ===
    ("pg211-sd-fec.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/sd_fec/v1_1/pg211-sd-fec.pdf", "Security"),
    
    # === Debug & Verification ===
    ("pg245-ila.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/ila/v6_2/pg172-ila.pdf", "Debug"),
    ("pg246-vio.pdf", "https://www.xilinx.com/support/documentation/ip_documentation/vio/v3_0/pg159-vio.pdf", "Debug"),
]

def download_pdf(item, timeout=60):
    """PDF dosyasını indir"""
    filename, url, category = item
    filepath = DOCS_DIR / filename
    
    if filepath.exists():
        size_kb = filepath.stat().st_size / 1024
        if size_kb > 10:  # En az 10 KB olmalı (gerçek PDF)
            print(f"✓ [{category}] Zaten var: {filename} ({size_kb:.1f} KB)")
            return True, filename, category
    
    try:
        print(f"⬇ [{category}] İndiriliyor: {filename}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            
        # PDF kontrolü
        if not content.startswith(b'%PDF'):
            print(f"⚠ [{category}] HTML döndü (PDF değil): {filename}")
            return False, filename, category
            
        with open(filepath, 'wb') as f:
            f.write(content)
            
        size_kb = len(content) / 1024
        print(f"✓ [{category}] İndirildi: {filename} ({size_kb:.1f} KB)")
        return True, filename, category
        
    except urllib.error.HTTPError as e:
        print(f"✗ [{category}] HTTP {e.code}: {filename}")
        return False, filename, category
    except Exception as e:
        print(f"✗ [{category}] Hata: {filename} - {str(e)[:50]}")
        return False, filename, category

def main():
    print("="*70)
    print("Xilinx IP Core Dökümanları İndiriliyor")
    print("="*70)
    print(f"Hedef dizin: {DOCS_DIR}")
    print(f"Toplam doküman: {len(ALL_IP_DOCS)}")
    print("="*70)
    print()
    
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }
    
    # Kategorilere göre grupla
    by_category = {}
    for item in ALL_IP_DOCS:
        cat = item[2]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)
    
    print(f"📂 Kategoriler: {', '.join(by_category.keys())}\n")
    
    # Sırayla indir (paralel indirme yerine, rate limit için)
    for i, item in enumerate(ALL_IP_DOCS, 1):
        filename, url, category = item
        print(f"[{i}/{len(ALL_IP_DOCS)}] ", end="")
        
        success, fname, cat = download_pdf(item)
        
        if success:
            results['success'].append((fname, cat))
        else:
            results['failed'].append((fname, cat))
        
        # Rate limiting - sunucuyu yormamak için
        if i < len(ALL_IP_DOCS):
            time.sleep(0.5)
        
        print()
    
    # Özet
    print("\n" + "="*70)
    print("İNDİRME TAMAMLANDI")
    print("="*70)
    print(f"✅ Başarılı: {len(results['success'])}")
    print(f"❌ Başarısız: {len(results['failed'])}")
    print(f"📊 Toplam: {len(ALL_IP_DOCS)}")
    print("="*70)
    
    # Kategoriye göre başarılı indirmeler
    print("\n📊 Kategoriye Göre Başarılı İndirmeler:")
    cat_stats = {}
    for fname, cat in results['success']:
        cat_stats[cat] = cat_stats.get(cat, 0) + 1
    
    for cat, count in sorted(cat_stats.items()):
        print(f"  {cat:15s}: {count:2d} doküman")
    
    # İndirilen dosyalar
    downloaded_files = sorted(DOCS_DIR.glob("*.pdf"))
    total_size_mb = sum(f.stat().st_size for f in downloaded_files) / (1024 * 1024)
    
    print(f"\n💾 Toplam boyut: {total_size_mb:.2f} MB")
    print(f"📁 Klasör: {DOCS_DIR}")
    
    # Başarısız olanları listele
    if results['failed']:
        print(f"\n⚠ Başarısız indirmeler ({len(results['failed'])} adet):")
        for fname, cat in results['failed'][:10]:  # İlk 10'u göster
            print(f"  - [{cat}] {fname}")
        if len(results['failed']) > 10:
            print(f"  ... ve {len(results['failed']) - 10} tane daha")

if __name__ == "__main__":
    main()
