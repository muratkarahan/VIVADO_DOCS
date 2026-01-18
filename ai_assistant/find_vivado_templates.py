"""
Vivado altındaki tüm template, IP core ve HDL örnek dosyalarını bul ve listele
"""
from pathlib import Path
from collections import defaultdict
import re

VIVADO_PATH = Path("C:/Xilinx/2025.1/Vivado")

print("=" * 100)
print("🔍 VIVADO TEMPLATE VE IP CORE DOSYALARI TARANYOR...")
print("=" * 100)

# Kategoriler
categories = {
    'verilog_examples': [],
    'vhdl_examples': [],
    'ip_templates': [],
    'design_examples': [],
    'testbenches': []
}

# IP core dizinleri
ip_cores = defaultdict(list)

# Verilog/SystemVerilog dosyaları
print("\n📁 Verilog/SystemVerilog dosyaları taranıyor...")
for ext in ['*.v', '*.vh', '*.sv']:
    for f in VIVADO_PATH.rglob(ext):
        path_str = str(f).lower()
        
        # Template veya example içeren dosyalar
        if any(keyword in path_str for keyword in ['template', 'example', 'demo', 'sample']):
            if 'testbench' in path_str or '_tb' in path_str:
                categories['testbenches'].append(f)
            elif 'example_design' in path_str:
                categories['design_examples'].append(f)
            else:
                categories['verilog_examples'].append(f)
            
            # IP core bilgisi
            if 'ip/xilinx' in path_str:
                parts = str(f).split('ip\\xilinx\\')
                if len(parts) > 1:
                    ip_name = parts[1].split('\\')[0]
                    ip_cores[ip_name].append(f)

# VHDL dosyaları
print("📁 VHDL dosyaları taranıyor...")
for ext in ['*.vhd', '*.vhdl']:
    for f in VIVADO_PATH.rglob(ext):
        path_str = str(f).lower()
        
        if any(keyword in path_str for keyword in ['template', 'example', 'demo', 'sample']):
            if 'testbench' in path_str or '_tb' in path_str:
                categories['testbenches'].append(f)
            elif 'example_design' in path_str:
                categories['design_examples'].append(f)
            else:
                categories['vhdl_examples'].append(f)
            
            # IP core bilgisi
            if 'ip\\xilinx' in str(f):
                parts = str(f).split('ip\\xilinx\\')
                if len(parts) > 1:
                    ip_name = parts[1].split('\\')[0]
                    ip_cores[ip_name].append(f)

# Sonuçları göster
print("\n" + "=" * 100)
print("📊 ÖZET")
print("=" * 100)

total = 0
for cat, files in categories.items():
    count = len(files)
    total += count
    cat_name = cat.replace('_', ' ').title()
    print(f"{cat_name:30s}: {count:5d} dosya")

print(f"{'TOPLAM':30s}: {total:5d} dosya")

print("\n" + "=" * 100)
print("🔧 IP CORE'LAR (Template/Örnek İçeren)")
print("=" * 100)

sorted_ips = sorted(ip_cores.items(), key=lambda x: len(x[1]), reverse=True)
for ip_name, files in sorted_ips[:30]:  # İlk 30
    print(f"{ip_name:40s}: {len(files):3d} dosya")

if len(sorted_ips) > 30:
    print(f"\n... ve {len(sorted_ips) - 30} IP core daha")

print(f"\nToplam IP Core: {len(ip_cores)}")

# Detaylı liste kaydet
print("\n" + "=" * 100)
print("💾 Detaylı liste kaydediliyor...")
print("=" * 100)

output_file = Path("vivado_templates_list.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 100 + "\n")
    f.write("VIVADO TEMPLATE VE IP CORE DOSYALARI - DETAYLI LİSTE\n")
    f.write("=" * 100 + "\n\n")
    
    # Kategorilere göre
    for cat, files in categories.items():
        if files:
            f.write(f"\n{'=' * 100}\n")
            f.write(f"{cat.replace('_', ' ').upper()}\n")
            f.write(f"{'=' * 100}\n")
            f.write(f"Toplam: {len(files)} dosya\n\n")
            
            for file in sorted(files):
                f.write(f"{file}\n")
    
    # IP Core'lara göre
    f.write(f"\n\n{'=' * 100}\n")
    f.write("IP CORE'LARA GÖRE DOSYALAR\n")
    f.write(f"{'=' * 100}\n\n")
    
    for ip_name, files in sorted_ips:
        f.write(f"\n{ip_name} ({len(files)} dosya):\n")
        f.write("-" * 80 + "\n")
        for file in sorted(files):
            f.write(f"  {file.name}\n")

print(f"✅ Detaylı liste kaydedildi: {output_file}")

print("\n" + "=" * 100)
print("✨ TARAMA TAMAMLANDI")
print("=" * 100)
