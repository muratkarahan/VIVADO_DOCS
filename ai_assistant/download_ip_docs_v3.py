"""
AMD/Xilinx IP Core PDF İndirme - Güncel Çalışan Linkler
"""

import os
from pathlib import Path
import time
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

DOCS_DIR = Path(r"C:\Users\murat\Documents\GitHub\VIVADO_DOCS\official_docs\IP_Cores")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Çalışan IP doküman linkleri - v7_1, v4_1 gibi versiyonlarla
WORKING_IP_DOCS = [
    # === AXI ===
    ("pg036-axi-bram-ctrl.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_bram_ctrl/v4_1/pg036-axi-bram-ctrl.pdf",
     "AXI BRAM Controller"),
    
    ("pg037-axi-pcie.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_pcie/v2_9/pg037-axi-pcie.pdf",
     "AXI PCIe Bridge"),
    
    ("pg055-axi-clock-converter.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_clock_converter/v2_1/pg055-axi-clock-converter.pdf",
     "AXI Clock Converter"),
    
    ("pg056-axi-dwidth-converter.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_dwidth_converter/v2_1/pg056-axi-dwidth-converter.pdf",
     "AXI Data Width Converter"),
    
    ("pg059-axi-crossbar.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_crossbar/v2_1/pg059-axi-crossbar.pdf",
     "AXI Crossbar"),
    
    ("pg085-axi-fifo-mm-s.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_fifo_mm_s/v4_2/pg085-axi-fifo-mm-s.pdf",
     "AXI Stream FIFO"),
    
    ("pg090-axi-iic.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_iic/v2_1/pg090-axi-iic.pdf",
     "AXI IIC"),
    
    ("pg099-axi-dma.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_dma/v7_1/pg099-axi-dma.pdf",
     "AXI DMA v7.1"),
    
    # === Memory ===
    ("pg058-blk-mem-gen.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/blk_mem_gen/v8_4/pg058-blk-mem-gen.pdf",
     "Block Memory Generator"),
    
    ("pg057-fifo-generator.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/fifo_generator/v13_2/pg057-fifo-generator.pdf",
     "FIFO Generator"),
    
    # === Ethernet ===
    ("pg138-ten-gig-eth-mac.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/ten_gig_eth_mac/v15_1/pg138-ten-gig-eth-mac.pdf",
     "10G Ethernet MAC"),
    
    ("pg051-axi-ethernet.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_ethernet/v7_2/pg051-axi-ethernet.pdf",
     "AXI Ethernet Lite"),
    
    # === DSP ===
    ("pg060-fir-compiler.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/fir_compiler/v7_2/pg060-fir-compiler.pdf",
     "FIR Compiler"),
    
    ("pg104-cordic.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/cordic/v6_0/pg104-cordic.pdf",
     "CORDIC"),
    
    ("pg105-cmpy.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/cmpy/v6_0/pg105-cmpy.pdf",
     "Complex Multiplier"),
    
    ("pg108-c-addsub.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/c_addsub/v12_0/pg108-c-addsub.pdf",
     "Adder/Subtractor"),
    
    ("pg109-mult-gen.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/mult_gen/v12_0/pg109-mult-gen.pdf",
     "Multiplier"),
    
    ("pg111-div-gen.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/div_gen/v5_1/pg111-div-gen.pdf",
     "Divider Generator"),
    
    ("pg121-floating-point.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/floating_point/v7_1/pg121-floating-point.pdf",
     "Floating Point"),
    
    ("pg141-dds-compiler.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/dds_compiler/v6_0/pg141-dds-compiler.pdf",
     "DDS Compiler"),
    
    ("pg149-xfft.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/xfft/v9_1/pg149-xfft.pdf",
     "FFT"),
    
    # === Serial ===
    ("pg046-aurora-8b10b.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/aurora_8b10b/v11_1/pg046-aurora-8b10b.pdf",
     "Aurora 8B/10B"),
    
    ("pg168-aurora-64b66b.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/aurora_64b66b/v12_0/pg168-aurora-64b66b.pdf",
     "Aurora 64B/66B"),
    
    # === Clock & Reset ===
    ("pg064-proc-sys-reset.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/proc_sys_reset/v5_0/pg064-proc-sys-reset.pdf",
     "Processor System Reset"),
    
    ("pg065-clk-wiz.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/clk_wiz/v6_0/pg065-clk-wiz.pdf",
     "Clocking Wizard"),
    
    # === Debug ===
    ("pg172-ila.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/ila/v6_2/pg172-ila.pdf",
     "ILA"),
    
    ("pg163-axis-jtag-debug.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axis_jtag_debug/v1_0/pg163-axis-jtag-debug.pdf",
     "JTAG to AXI Master"),
    
    # === PCIe ===
    ("pg054-axi-pcie.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_pcie/v2_9/pg054-axi-pcie.pdf",
     "AXI Bridge for PCIe"),
    
    ("pg195-pcie-dma.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/pcie_dma/v4_1/pg195-pcie-dma.pdf",
     "DMA Subsystem for PCIe"),
    
    # === Video ===
    ("pg044-v-tc.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/v_tc/v6_1/pg044-v-tc.pdf",
     "Video Timing Controller"),
    
    ("pg278-hdmi-tx-ss.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/hdmi_tx_ss/v3_1/pg278-hdmi-tx-ss.pdf",
     "HDMI TX Subsystem"),
    
    ("pg279-hdmi-rx-ss.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/hdmi_rx_ss/v3_1/pg279-hdmi-rx-ss.pdf",
     "HDMI RX Subsystem"),
    
    # === Timer ===
    ("pg078-axi-timer.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_timer/v2_0/pg078-axi-timer.pdf",
     "AXI Timer"),
    
    ("pg079-axi-intc.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/axi_intc/v4_1/pg079-axi-intc.pdf",
     "AXI Interrupt Controller"),
    
    # === MIG ===
    ("ug586-7series-mis.pdf",
     "https://www.xilinx.com/content/dam/xilinx/support/documents/ip_documentation/mig_7series/v4_2/ug586_7Series_MIS.pdf",
     "7 Series MIG"),
]

def download_pdf(item, timeout=120):
    """PDF dosyasını indir"""
    filename, url, description = item
    filepath = DOCS_DIR / filename
    
    if filepath.exists():
        size_kb = filepath.stat().st_size / 1024
        if size_kb > 100:
            print(f"✓ Zaten var: {filename} ({size_kb:.1f} KB)")
            return True, filename
    
    try:
        print(f"⬇ İndiriliyor: {filename} - {description}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/pdf,*/*',
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            
        if content.startswith(b'%PDF'):
            with open(filepath, 'wb') as f:
                f.write(content)
            size_kb = len(content) / 1024
            print(f"✓ İndirildi: {filename} ({size_kb:.1f} KB)")
            return True, filename
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
    print("AMD/Xilinx IP Core PDF İndirme v3")
    print("="*70)
    print(f"Hedef: {DOCS_DIR}")
    print(f"Toplam: {len(WORKING_IP_DOCS)} doküman")
    print("="*70 + "\n")
    
    success = 0
    failed = 0
    
    for i, item in enumerate(WORKING_IP_DOCS, 1):
        print(f"[{i}/{len(WORKING_IP_DOCS)}] ", end="")
        result, _ = download_pdf(item)
        if result:
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
