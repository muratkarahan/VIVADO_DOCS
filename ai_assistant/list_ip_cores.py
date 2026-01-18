"""
Xilinx IP Core örneklerini bul ve listele
"""
from pathlib import Path
from collections import defaultdict

VIVADO_IP_PATH = Path("C:/Xilinx/2025.1/Vivado/data/ip/xilinx")

print("=" * 100)
print("🔍 XILINX IP CORE'LAR TARANYOR...")
print("=" * 100)

# Tüm IP core'ları bul
ip_cores = list(VIVADO_IP_PATH.glob("*"))
print(f"\n📊 Toplam IP Core: {len(ip_cores)}")

# Örnek içeren IP'leri bul
ip_with_examples = {}
ip_with_hdl = {}

for ip_dir in ip_cores:
    if not ip_dir.is_dir():
        continue
    
    ip_name = ip_dir.name
    
    # Example dizinleri ara
    example_dirs = list(ip_dir.rglob("*example*")) + list(ip_dir.rglob("*demo*"))
    example_dirs = [d for d in example_dirs if d.is_dir()]
    
    # HDL dosyaları ara
    hdl_files = []
    for ext in ['*.v', '*.vh', '*.sv', '*.vhd']:
        hdl_files.extend(list(ip_dir.rglob(ext)))
    
    if example_dirs:
        ip_with_examples[ip_name] = {
            'example_dirs': example_dirs,
            'hdl_files': [f for f in hdl_files if any(e in str(f).lower() for e in ['example', 'demo'])]
        }
    elif hdl_files:
        ip_with_hdl[ip_name] = hdl_files

print(f"📁 Örnek içeren IP Core: {len(ip_with_examples)}")
print(f"🔧 HDL dosyası olan IP Core: {len(ip_with_hdl)}")

# Kategorize et
categories = {
    'Connectivity': ['axi', 'ahb', 'apb', 'pcie', 'ethernet', 'usb', 'aurora'],
    'Video & Graphics': ['vid', 'video', 'hdmi', 'display', 'graphics', 'tpg'],
    'DSP & Math': ['dsp', 'fft', 'fir', 'cordic', 'dds', 'math'],
    'Memory': ['ddr', 'memory', 'mig', 'bram', 'fifo', 'qdr'],
    'Processing': ['microblaze', 'processor', 'zynq', 'versal'],
    'Other': []
}

categorized_ips = defaultdict(list)

for ip_name in ip_with_examples.keys():
    categorized = False
    for cat, keywords in categories.items():
        if cat == 'Other':
            continue
        if any(kw in ip_name.lower() for kw in keywords):
            categorized_ips[cat].append(ip_name)
            categorized = True
            break
    if not categorized:
        categorized_ips['Other'].append(ip_name)

# Sonuçları göster
print("\n" + "=" * 100)
print("📂 KATEGORİLERE GÖRE ÖRNEK İÇEREN IP CORE'LAR")
print("=" * 100)

for cat in ['Connectivity', 'Video & Graphics', 'DSP & Math', 'Memory', 'Processing', 'Other']:
    if categorized_ips[cat]:
        print(f"\n🔹 {cat} ({len(categorized_ips[cat])} IP)")
        print("-" * 100)
        for ip in sorted(categorized_ips[cat])[:10]:
            info = ip_with_examples[ip]
            print(f"  • {ip:50s} ({len(info['hdl_files'])} HDL dosyası)")
        if len(categorized_ips[cat]) > 10:
            print(f"  ... ve {len(categorized_ips[cat]) - 10} IP daha")

# Detaylı liste
print("\n" + "=" * 100)
print("📋 ÖNEMLİ IP CORE'LAR VE ÖRNEKLERİ")
print("=" * 100)

important_ips = [
    'axi_ethernet', 'axi_dma', 'axi_gpio', 'axi_uartlite', 'axi_iic',
    'mig_7series', 'ddr4', 'axi_bram_ctrl', 'fifo_generator',
    'clk_wiz', 'proc_sys_reset', 'blk_mem_gen',
    'axi_interconnect', 'smartconnect'
]

for ip_pattern in important_ips:
    matching_ips = [ip for ip in ip_with_examples.keys() if ip_pattern in ip.lower()]
    
    if matching_ips:
        for ip_name in matching_ips[:1]:  # İlk eşleşen
            info = ip_with_examples[ip_name]
            print(f"\n🔸 {ip_name}")
            print(f"   Example dizinler: {len(info['example_dirs'])}")
            print(f"   HDL dosyaları: {len(info['hdl_files'])}")
            
            if info['hdl_files']:
                print(f"   Örnek dosyalar:")
                for f in info['hdl_files'][:5]:
                    print(f"      • {f.name}")

# Kaydet
print("\n" + "=" * 100)
print("💾 IP Core listesi kaydediliyor...")
print("=" * 100)

output_file = Path("vivado_ip_cores_list.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 100 + "\n")
    f.write("XILINX VIVADO IP CORE'LAR - DETAYLI LİSTE\n")
    f.write("=" * 100 + "\n\n")
    
    f.write(f"Toplam IP Core: {len(ip_cores)}\n")
    f.write(f"Örnek içeren IP Core: {len(ip_with_examples)}\n")
    f.write(f"HDL dosyası olan IP Core: {len(ip_with_hdl)}\n\n")
    
    f.write("=" * 100 + "\n")
    f.write("ÖRNEK İÇEREN IP CORE'LAR\n")
    f.write("=" * 100 + "\n\n")
    
    for ip_name in sorted(ip_with_examples.keys()):
        info = ip_with_examples[ip_name]
        f.write(f"\n{ip_name}\n")
        f.write("-" * 80 + "\n")
        f.write(f"Example dizinler: {len(info['example_dirs'])}\n")
        f.write(f"HDL dosyaları: {len(info['hdl_files'])}\n")
        
        if info['hdl_files']:
            f.write("\nÖrnek dosyalar:\n")
            for hdl in info['hdl_files'][:10]:
                f.write(f"  • {hdl}\n")
            if len(info['hdl_files']) > 10:
                f.write(f"  ... ve {len(info['hdl_files']) - 10} dosya daha\n")
        f.write("\n")
    
    f.write("\n" + "=" * 100 + "\n")
    f.write("TÜM IP CORE'LAR (Alfabetik)\n")
    f.write("=" * 100 + "\n\n")
    
    for ip_dir in sorted(ip_cores):
        f.write(f"{ip_dir.name}\n")

print(f"✅ IP Core listesi kaydedildi: {output_file}")

print("\n" + "=" * 100)
print("✨ TARAMA TAMAMLANDI")
print("=" * 100)
