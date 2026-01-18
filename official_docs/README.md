# Xilinx Vivado Resmi Dökümanları

Bu klasör Xilinx/AMD'nin resmi Vivado Design Suite dökümanlarını içerir.

## 📁 Klasör Yapısı

```
official_docs/
├── Design_Tools/          # Vivado, Vitis, HLS kullanım kılavuzları
├── IP_Cores/              # IP Core datasheet ve user guide'ları
├── SoC_Embedded/          # Zynq, UltraScale+ MPSoC dökümanları
├── Transceivers/          # GTH/GTY/GTX transceiver rehberleri
└── Datasheets/            # FPGA datasheet'leri
```

## 📥 Dökümanları İndirme

### Design Tools (Vivado/Vitis)

**Xilinx Downloads:** https://www.xilinx.com/support/documentation.html

#### Temel Kılavuzlar:
- **UG835** - Vivado Design Suite Tcl Command Reference Guide
- **UG892** - Vivado Design Suite User Guide: Design Flows Overview
- **UG893** - Vivado Design Suite User Guide: Using the Vivado IDE
- **UG894** - Vivado Design Suite User Guide: Using Constraints
- **UG895** - Vivado Design Suite User Guide: I/O and Clock Planning
- **UG896** - Vivado Design Suite User Guide: Getting Started
- **UG897** - Vivado Design Suite User Guide: Model-Based DSP Design
- **UG898** - Vivado Design Suite User Guide: Embedded Processor Hardware Design
- **UG899** - Vivado Design Suite User Guide: I/O and Clock Planning
- **UG901** - Vivado Design Suite User Guide: Synthesis
- **UG904** - Vivado Design Suite User Guide: Implementation
- **UG906** - Vivado Design Suite User Guide: Design Analysis and Closure Techniques
- **UG910** - Vivado Design Suite User Guide: Programming and Debugging
- **UG912** - Vivado Design Suite Properties Reference Guide
- **UG949** - UltraFast Design Methodology Guide for FPGAs and SoCs
- **UG994** - Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator

#### Simulation:
- **UG900** - Vivado Design Suite User Guide: Logic Simulation
- **UG937** - Vivado Design Suite Tutorial: Logic Simulation

#### Vitis HLS:
- **UG1399** - Vitis HLS User Guide
- **UG1393** - Vitis Unified Software Platform Documentation

### IP Cores

#### AXI Infrastructure:
- **PG057** - AXI Interconnect v2.1
- **PG059** - AXI4-Stream Infrastructure
- **PG080** - AXI DMA v7.1
- **PG150** - AXI SmartConnect

#### Memory & Storage:
- **PG058** - FIFO Generator v13.2
- **PG065** - Block Memory Generator v8.4
- **PG150** - MIG 7 Series
- **PG150** - UltraScale FPGAs Memory Interface Solutions

#### Clocking:
- **PG065** - Clocking Wizard v6.0
- **UG472** - 7 Series FPGAs Clocking Resources

#### Communication:
- **PG034** - Tri-Mode Ethernet MAC v9.0
- **PG157** - 1G/2.5G Ethernet PCS/PMA or SGMII
- **PG203** - 10G/25G Ethernet Subsystem

#### Video & Display:
- **PG098** - Video Timing Controller
- **PG122** - Video Processing Subsystem

#### DSP:
- **PG060** - FFT v9.1
- **PG105** - FIR Compiler v7.2

### SoC & Embedded

#### Zynq-7000:
- **UG585** - Zynq-7000 SoC Technical Reference Manual
- **UG1046** - Zynq-7000 SoC Embedded Design Tutorial

#### Zynq UltraScale+ MPSoC:
- **UG1085** - Zynq UltraScale+ MPSoC Technical Reference Manual
- **UG1209** - Zynq UltraScale+ MPSoC Embedded Design Tutorial

#### PetaLinux:
- **UG1144** - PetaLinux Tools Documentation Reference Guide
- **UG1157** - PetaLinux Tools Documentation: Workflow Tutorial

#### Vitis Embedded:
- **UG1400** - Vitis Embedded Software Development Flow Documentation

### Transceivers

#### 7-Series:
- **UG476** - 7 Series FPGAs GTX/GTH Transceivers

#### UltraScale/UltraScale+:
- **UG576** - UltraScale Architecture GTH Transceivers
- **UG578** - UltraScale Architecture GTY Transceivers
- **PG182** - UltraScale+ GTY Transceivers

### Datasheets

#### 7-Series:
- **DS180** - Artix-7 FPGAs Data Sheet
- **DS181** - Kintex-7 FPGAs Data Sheet
- **DS182** - Virtex-7 FPGAs Data Sheet
- **DS190** - Zynq-7000 SoC Data Sheet

#### UltraScale:
- **DS890** - Kintex UltraScale FPGAs Data Sheet
- **DS891** - Virtex UltraScale FPGAs Data Sheet

#### UltraScale+:
- **DS922** - Kintex UltraScale+ FPGAs Data Sheet
- **DS923** - Virtex UltraScale+ FPGAs Data Sheet
- **DS925** - Zynq UltraScale+ MPSoC Data Sheet

## 📋 İndirme Checklist

### Zorunlu (Minimum Set):
- [ ] UG835 - TCL Command Reference
- [ ] UG949 - UltraFast Methodology
- [ ] UG994 - IP Integrator
- [ ] PG057 - AXI Interconnect
- [ ] PG058 - FIFO Generator
- [ ] PG080 - AXI DMA
- [ ] UG585 - Zynq-7000 TRM (eğer Zynq kullanıyorsanız)

### Tavsiye Edilen:
- [ ] UG901 - Synthesis
- [ ] UG904 - Implementation
- [ ] UG906 - Design Analysis
- [ ] UG912 - Properties Reference
- [ ] UG1399 - Vitis HLS
- [ ] UG1085 - Zynq UltraScale+ TRM

### Projeye Özel:
- İlgili IP Core dökümanları
- Kullanılan FPGA datasheet'i
- Transceiver guide'ları (yüksek hızlı IO varsa)

## 🔄 Güncelleme

Vivado versiyonları ile dökümanlar güncellenir. Her major release'de:
1. Xilinx Documentation Portal'ı kontrol edin
2. Kullandığınız Vivado versiyonuna uygun UG'leri indirin
3. `setup_vivado_ai.py --reindex` ile database'i güncelleyin

## 📊 Indexleme

Dökümanları indirdikten sonra:

```powershell
cd ai_assistant
python setup_vivado_ai.py
```

Bu script:
- PDF'leri okur
- Text extraction yapar
- Chunk'lara böler
- OpenAI embeddings oluşturur
- ChromaDB'ye yazar

## 💡 İpuçları

1. **PDF Kalitesi:** OCR'li taramalı PDF'ler yerine native PDF kullanın
2. **Versiyon Uyumu:** Kullandığınız Vivado versiyonuyla uyumlu dökümanları tercih edin
3. **Öncelik:** IP Integrator ve TCL kılavuzları en çok kullanılanlardır
4. **Boyut:** Tüm dökümanlar ~2-3 GB alan kaplar

## 📞 Yardım

Döküman bulamıyorsanız:
- Xilinx Answer Database: https://support.xilinx.com/s/
- Xilinx Forums: https://forums.xilinx.com/
- AMD Support: https://www.amd.com/en/support

---

**Not:** Bu dökümanlar Xilinx/AMD'nin telif hakkıdır. Yalnızca kişisel eğitim ve referans için kullanılmalıdır.
