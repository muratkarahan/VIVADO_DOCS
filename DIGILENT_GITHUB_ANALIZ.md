# Digilent GitHub Repository Analizi

**Tarih**: 31 Ocak 2026  
**Kaynak**: https://github.com/Digilent

---

## 📊 ÖZET İSTATİSTİKLER

### Toplam İndirilen Projeler (Workspace)
- **Toplam Repository**: 40 adet
- **Digilent Spesifik**: 24 adet
- **Diğer (Xilinx, vb.)**: 16 adet

### Dosya Türleri (Tüm Projeler)
| Dosya Türü | Sayı | Açıklama |
|------------|------|----------|
| **.XPR** | 23 | Vivado Project dosyaları |
| **.TCL** | 944 | TCL scriptleri (proje oluşturma, build) |
| **.XDC** | 464 | Constraint dosyaları (pin mapping, timing) |
| **.BD** | 21 | Block Design dosyaları |
| **.V** | 982 | Verilog kaynak dosyaları |
| **.VHD** | 408 | VHDL kaynak dosyaları |

### Sadece Digilent Projeleri
| Dosya Türü | Sayı |
|------------|------|
| **.XPR** | 0 ⚠️ |
| **.TCL** | 47 |
| **.XDC** | 23 |
| **.BD** | 1 |
| **.V** | 12 |
| **.VHD** | 57 |

> **Önemli Not**: Digilent projeleri doğrudan `.xpr` dosyası içermez, bunun yerine **TCL scriptleri** ile proje oluşturulur!

---

## 🎯 İndirilen Digilent Board Repoları

### 1. Zynq-7000 SoC Platformları
| Repository | Stars | Açıklama |
|-----------|-------|----------|
| **Zybo-Z7** | ⭐ 31 | Zynq-7020 dev board |
| **Arty-Z7** | ⭐ 3 | Kompakt Zynq-7020 board |
| **Cora-Z7** | ⭐ 5 | Minimal Zynq-7007S/7010 |
| **Eclypse-Z7** | ⭐ 21 | High-speed ADC/DAC |

### 2. Artix-7 & Spartan-7 Platformları
| Repository | Stars | Açıklama |
|-----------|-------|----------|
| **Arty-S7** | ⭐ 9 | Spartan-7 entry-level |
| **Basys-3** | ⭐ 13 | Eğitim amaçlı Artix-7 |
| **Nexys-A7** | ⭐ 15 | Gelişmiş Artix-7 |

### 3. Kintex & Ultrascale+ Platformları
| Repository | Stars | Açıklama |
|-----------|-------|----------|
| **Genesys-2** | ⭐ 7 | Kintex-7 high-end |
| **Genesys-ZU** | ⭐ 14 | Zynq UltraScale+ MPSoC |

---

## 📦 İndirilen Demo Projeleri

### Kamera & Video
- **Zybo-Z7-20-pcam-5c** ⭐ 58 - PCAM 5C kamera demo
  - 7 TCL, 4 XDC, 1 BD
  - Bayer to RGB, Gamma düzeltme IP'leri
  
- **Zybo-Z7-20-HDMI** ⭐ 25 - HDMI video demo
  - 2 TCL, 1 XDC

### Pmod Örnekleri
- **Pmod-I2S2** ⭐ 48 - Audio codec demo
  - 8 TCL, 7 XDC

### DMA & ADC
- **Zybo-Z7-10-DMA** ⭐ 7 - DMA veri transferi
  - 3 TCL, 2 XDC
  
- **Zybo-Z7-10-XADC** ⭐ 6 - XADC sensör okuma
  - 1 TCL, 1 XDC
  
- **Arty-A7-100-XADC** ⭐ 5 - Artix-7 XADC
  - 1 TCL, 1 XDC

---

## 🛠️ Hardware (HW) Repoları

Digilent'in **-HW** repoları doğrudan Vivado proje dosyaları içermez, ancak:

| Repository | Dosyalar |
|-----------|----------|
| **Eclypse-Z7-HW** | 2 TCL, 1 XDC |
| **Arty-A7-HW** | 0 dosya (README only) |
| **Zybo-Z7-HW** | 0 dosya (README only) |
| **Genesys-ZU-HW** | 0 dosya (README only) |
| **Basys-3-HW** | 0 dosya (README only) |
| **Nexys-Video-HW** | 0 dosya (README only) |

> **Neden HW repoları boş?** Digilent, board tanımlarını `vivado-boards` repo'sunda tutar, örnekleri ise ayrı repolarda.

---

## 🔧 Digilent Araç Repoları

### vivado-boards ⭐ 485
- **Boyut**: 3.3 MB
- **İçerik**: 154 dosya, 3 TCL
- **Amaç**: Tüm Digilent boardları için Vivado board definition dosyaları
- **Kullanım**: `C:\Xilinx\Vivado\<version>\data\boards\board_files\` altına kopyalanır

### digilent-vivado-scripts ⭐ 70
- **Boyut**: 0.1 MB
- **İçerik**: 10 dosya, 4 TCL
- **Amaç**: Git-friendly Vivado proje yönetimi
- **Özellikler**:
  - `digilent_vivado_checkout.tcl` - Git'ten proje oluşturma
  - `digilent_vivado_checkin.tcl` - Proje export
  - Version control için binary dosyaları çıkarır

### vivado-library ⭐ 666
- **Boyut**: 2.3 MB
- **İçerik**: 86 dosya, 16 TCL, 6 XDC
- **Amaç**: Digilent IP core kütüphanesi
- **IP'ler**:
  - Pmod IP'leri (I2S, SPI, UART, etc.)
  - Video IP'leri (RGB to DVI, etc.)
  - Utility IP'leri

### digilent-xdc ⭐ 643
- **Boyut**: TCL formatında
- **İçerik**: Tüm Digilent boardları için master XDC dosyaları
- **Boards**: Arty, Basys, Cmod, Cora, Eclypse, Genesys, Nexys, Zybo, ZedBoard
- **Kullanım**: Pin constraint şablonları

---

## 📋 Proje Oluşturma Yaklaşımı

Digilent **`.xpr` dosyası paylaşmaz**, bunun yerine:

### 1️⃣ TCL Script Yaklaşımı (Tercih Edilen)
```tcl
# Örnek: Zybo-Z7-20-pcam-5c/proj/create_project.tcl
source ../repo/vivado-library/ip/create_ip.tcl
source ./system.tcl

create_project pcam_vdma_proj ./proj -part xc7z020clg400-1
add_files -fileset constrs_1 -norecurse ./src/constraints/auto.xdc
```

**Avantajlar**:
- ✅ Git-friendly (binary yok)
- ✅ Version kontrolü kolay
- ✅ Farklı Vivado versiyonlarında çalışır
- ✅ Otomatik build pipeline'a entegre

### 2️⃣ Block Design (.bd) Kullanımı
```tcl
create_bd_design "design_1"
# IP'leri ekle, bağlantıları yap
```

**IP Integrator** ile görsel tasarım, `.bd` dosyası olarak saklanır.

---

## 🔍 Dosya Yapısı Örneği

### Tipik Bir Digilent Projesi (Zybo-Z7-20-pcam-5c):
```
Zybo-Z7-20-pcam-5c/
├── README.md
├── proj/
│   ├── create_project.tcl        # Ana TCL script
│   ├── system.tcl                 # Sistem konfigürasyonu
│   └── cleanup.cmd                # Temizleme
├── repo/
│   └── (vivado-library linkı)
├── src/
│   ├── bd/
│   │   └── design_1.bd           # Block Design
│   ├── constraints/
│   │   ├── auto.xdc              # Otomatik constraint
│   │   ├── timing.xdc            # Timing constraint
│   │   └── *.xdc
│   ├── hdl/
│   │   ├── *.vhd                 # VHDL kaynakları
│   │   └── *.v                   # Verilog kaynakları
│   └── ip/
│       └── AXI_*                 # Custom IP'ler
└── sdk/
    └── (Software projects)
```

---

## 💡 Proje Nasıl Oluşturulur?

### Adım 1: Repository'yi Klonla
```bash
git clone https://github.com/Digilent/Zybo-Z7-20-pcam-5c
cd Zybo-Z7-20-pcam-5c
```

### Adım 2: Vivado'da TCL Çalıştır
**Vivado TCL Console'da**:
```tcl
cd proj
source ./create_project.tcl
```

VEYA **Komut satırından**:
```bash
vivado -mode batch -source proj/create_project.tcl
```

### Adım 3: Projeyi Aç
Vivado otomatik olarak `.xpr` dosyasını oluşturur:
```
proj/pcam_vdma_proj/pcam_vdma_proj.xpr
```

---

## 📊 Digilent vs Diğer Projeler Karşılaştırma

| Özellik | Digilent | Xilinx Official | Diğer (eugene-tarassov, vb.) |
|---------|----------|-----------------|------------------------------|
| **XPR Dosyası** | ❌ TCL ile oluştur | ✅ Bazen var | ✅ Çoğunlukla var |
| **TCL Script** | ✅ Her projede | ✅ Genelde var | ⚠️ Bazen |
| **Git Friendly** | ✅ Tamamen | ⚠️ Kısmen | ❌ Binary dosyalar |
| **Board Tanımı** | ✅ vivado-boards | ✅ Built-in | ⚠️ Manual |
| **IP Library** | ✅ vivado-library | ✅ Built-in | ⚠️ Proje içinde |
| **Dokümantasyon** | ✅ Mükemmel | ✅ İyi | ⚠️ Değişken |

---

## 🎓 Önerilen Başlangıç Projeleri

### Yeni Başlayanlar:
1. **Basys-3** - En basit FPGA board, LED/Button örnekleri
2. **Arty-A7-100-XADC** - ADC okuma örneği
3. **Zybo-Z7-10-DMA** - PS-PL veri transferi

### Orta Seviye:
4. **Zybo-Z7-20-HDMI** - Video pipeline
5. **Pmod-I2S2** - Audio codec kullanımı
6. **Zybo-Z7-10-XADC** - Analog sensör okuma

### İleri Seviye:
7. **Zybo-Z7-20-pcam-5c** - Kamera, IP Integrator, custom IP
8. **Eclypse-Z7-HW** - High-speed ADC/DAC
9. **Genesys-ZU-HW** - UltraScale+ MPSoC

---

## 🔗 Önemli Linkler

### Digilent Ana Repoları
- **Board Definitions**: https://github.com/Digilent/vivado-boards
- **Vivado Scripts**: https://github.com/Digilent/digilent-vivado-scripts
- **IP Library**: https://github.com/Digilent/vivado-library
- **XDC Files**: https://github.com/Digilent/digilent-xdc

### Dokümantasyon
- **Reference Manual**: https://digilent.com/reference/programmable-logic/documents/git
- **Getting Started**: Her board repo'sunda README.md

---

## ✅ Sonuç

### ❌ Digilent'te Neden .XPR Yok?
Digilent'in stratejik kararı:
- **Git uyumluluğu**: Binary `.xpr` dosyaları merge conflict yaratır
- **Vivado versiyon bağımsızlığı**: TCL her versiyonda çalışır
- **Temiz repo**: Sadece kaynak dosyalar, generated dosyalar yok
- **CI/CD entegrasyonu**: Otomatik build pipeline için ideal

### ✅ Ne Yapmalısınız?
1. ✅ **vivado-boards** repo'sunu Vivado'ya kurun
2. ✅ **vivado-library** kütüphanesini klonlayın
3. ✅ İlgilendiğiniz board demo'larını klonlayın
4. ✅ TCL scriptleri ile proje oluşturun
5. ✅ Oluşturulan `.xpr` dosyasını `.gitignore`'a ekleyin

### 📝 Workspace Yapısı Önerisi
```
VIVADO_DOCS/
├── digilent_boards/
│   └── vivado-boards/           # Board definitions
├── digilent_ips/
│   └── vivado-library/          # IP cores
├── digilent_projects/
│   ├── Zybo-Z7-20-pcam-5c/
│   ├── Arty-A7-100-XADC/
│   └── ...
└── my_projects/
    └── (sizin projeleriniz)
```

---

**Son Güncelleme**: 31 Ocak 2026  
**Toplam İndirilen Dosya Sayısı**: ~22,000  
**Toplam Boyut**: ~1.8 GB
