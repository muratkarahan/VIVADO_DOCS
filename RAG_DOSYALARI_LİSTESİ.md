# VIVADO RAG SİSTEMİ - DÖKÜMANLARIN DETAYLI LİSTESİ

Bu README dosyası, Vivado RAG (Retrieval-Augmented Generation) sistemi için toplanan, işlenen veya işlenmeye hazır tüm dokümanların detaylı listesini içerir.

---

## 📊 GENEL ÖZET

### Şu Anda RAG Sisteminde:
- **Toplam Döküman**: 1,492 chunk
- **Benzersiz Dosya**: 128 dosya
- **Toplam Token**: ~1.66 milyon
- **Eğitim Süresi**: ~15 dakika
- **Maliyet**: ~$0.17

### Hazır Ama Henüz Eklenmemiş:
- **Verilog/VHDL Template**: 118 dosya
- **IP Core Örnekleri**: 46 IP (597 toplam IP)
- **Xilinx PDF**: 26 PDF (9 benzersiz)

---

## 1️⃣ RAG SİSTEMİNE EKLENMİŞ DOSYALAR (128 Dosya)

### 📄 Xilinx Vivado Resmi Dokümanları (3 PDF)
**Kaynak**: `C:\Xilinx\2025.1\Vivado\ids_lite\ISE\coregen\ip\xilinx\other\com\xilinx\ip\mig_7series_v1_7\data\docs\`

1. `ds176_7Series_MIS.pdf` - 7-Series Memory Interface Solutions Datasheet
2. `ug586_7Series_MIS.pdf` - 7-Series Memory Interface Solutions User Guide  
3. `Version_Info.pdf` - MIG Version Information

---

### 📄 Xilinx Data Dokümanları (4 PDF)
**Kaynak**: `C:\Xilinx\2025.1\data\`

1. `xilflash.pdf` - Xilflash Embedded Software Library (embeddedsw/lib/sw_services/xilflash_v4_9/doc/)
2. `pci_32_ds206.pdf` - PCI 32-bit IP Datasheet (ip/xilinx/pci32_v5_0/doc/)
3. `pci_64_ds205.pdf` - PCI 64-bit IP Datasheet (ip/xilinx/pci64_v5_0/doc/)
4. `SystemC_Open_Source_License.pdf` - SystemC License (osci_systemc/include/)

---

### 📄 FPGA Proje Dokümanları

#### AX7010 Projesi (9 PDF)
**Kaynak**: `C:\Users\murat\Documents\GitHub\ax7010_fpga\`

1. `AD8065_8066.pdf` - Op-Amp Datasheet
2. `AD9280.pdf` - ADC Datasheet
3. `AD9708.pdf` - DAC Datasheet
4. `TL072.pdf` - Op-Amp Datasheet
5. `pg058-blk-mem-gen.pdf` - Block Memory Generator Product Guide
6. `pg065_clk_wiz.pdf` - Clocking Wizard Product Guide
7. `rgb2dvi_v1_2.pdf` - RGB to DVI Video IP
8. `ADDA原理图.pdf` - ADC/DAC Schematic
9. `取样电路.pdf` - Sampling Circuit

#### Z7Lite Projesi (9 PDF)
**Kaynak**: `C:\Users\murat\Documents\GitHub\z7lite_fpga\`

1. `UG471_7Series_SelectIO.pdf` - 7-Series SelectIO Resources User Guide
2. `UG768 7series_hdl.pdf` - 7-Series HDL Libraries Guide
3. `ADA106原理图.pdf` - ADA106 Schematic
4. `ADA106实验教程.pdf` - ADA106 Lab Tutorial
5. `ADA106用户手册.pdf` - ADA106 User Manual
6. `adc08100.pdf` - ADC08100 Datasheet
7. `dac908.pdf` - DAC908 Datasheet
8. `dvi2rgb.pdf` - DVI to RGB IP
9. `rgb2dvi.pdf` - RGB to DVI IP

#### Z7Nano Projesi (1 PDF)
**Kaynak**: `C:\Users\murat\Documents\GitHub\z7nano_fpga\`

1. `datasheet.pdf` - EEPROM Datasheet

#### docs_fpga (5 PDF)
**Kaynak**: `C:\Users\murat\Documents\GitHub\docs_fpga\`

1. `AX7010_User_Manual.pdf` - AX7010 Development Board User Manual
2. `AN108_User_Manual.pdf` - AN108 ADC/DAC Module User Manual
3. `Part1_Z7_Nano_Tutorial_Logic.pdf` - Zynq-7000 Nano Tutorial Part 1
4. `Part1_Z7-Lite_Tutorial_Logic.pdf` - Zynq-7000 Lite Tutorial Part 1
5. `course_s1_ALINX_ZYNQ(AX7010).pdf` - ALINX AX7010 Course Season 1

#### Diğer Projeler (2 PDF)
**Kaynak**: Çeşitli GitHub projeleri

1. `ZmodDigitizerController.pdf` - Zmod Digitizer Controller IP (coraz7_fpga)
2. `dvi2rgb.pdf` - DVI to RGB IP (nexsys_fpga)

---

### 📝 VIVADO_DOCS Workspace (7 Markdown)
**Kaynak**: `C:\Users\murat\Documents\GitHub\VIVADO_DOCS\`

1. `README.md` - Ana README
2. `KURULUM.md` - Kurulum kılavuzu
3. `DEMO_ORNEKLERI.md` - Demo örnekleri
4. `KOD_ORNEKLERI.md` - Kod örnekleri
5. `QUICKSTART.md` - Hızlı başlangıç kılavuzu
6. `RAG_TRAINING_GUIDE.md` - RAG eğitim kılavuzu
7. `OFFICIAL_DOCS_INDEX.md` - Resmi dokümanlar indeksi

---

### 📝 GitHub Proje Markdown Dokümanları (88 Dosya)
**Kaynak**: Çeşitli GitHub FPGA projeleri

README, CONTRIBUTING, CHANGELOG, AUTHORS, LICENSE ve diğer proje dokümanları.

**Örnekler**:
- README.md (çeşitli projelerden)
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- CHANGELOG.md
- AUTHORS.md
- BACKERS.md
- DEVELOPING.md
- ... (toplam 88 dosya)

---

## 2️⃣ HAZIR AMA HENÜZ EKLENMEMİŞ DOSYALAR

### 🔧 Verilog/SystemVerilog Template ve Örnekler (105 Dosya)
**Kaynak**: `C:\Xilinx\2025.1\Vivado\examples\`

#### Vivado Tutorial Örnekleri
**Konum**: `Vivado_Tutorial\Sources\hdl\`

##### OpenRISC 1200 CPU (56 dosya)
- `or1200_top.v` - OpenRISC 1200 Top Module
- `or1200_cpu.v` - CPU Core
- `or1200_alu.v` - ALU
- `or1200_ctrl.v` - Control Unit
- `or1200_if.v` - Instruction Fetch
- `or1200_except.v` - Exception Handling
- `or1200_immu_top.v` - Instruction MMU
- `or1200_dmmu_top.v` - Data MMU
- `or1200_ic_top.v` - Instruction Cache
- `or1200_dc_top.v` - Data Cache
- ... (toplam 56 dosya)

##### USB Function Controller (13 dosya)
- `usbf_top.v` - USB Function Top
- `usbf_pe.v` - Protocol Engine
- `usbf_pl.v` - Physical Layer
- `usbf_utmi_if.v` - UTMI Interface
- `usbf_crc16.v` - CRC16
- `usbf_crc5.v` - CRC5
- ... (13 dosya)

##### Wishbone Interconnect (9 dosya)
- `wb_conmax_top.v` - Wishbone Interconnect Top
- `wb_conmax_arb.v` - Arbiter
- `wb_conmax_master_if.v` - Master Interface
- `wb_conmax_slave_if.v` - Slave Interface
- ... (9 dosya)

##### MGT (Gigabit Transceiver) Örnekleri (5 dosya)
- `mgtTop.v`
- `rocketio_wrapper_tile.v`
- `rocketio_wrapper_tile_gt.v`
- `rocketio_wrapper_tile_gt_frame_check.v`
- `rocketio_wrapper_tile_gt_frame_gen.v`

##### Diğer Modüller
- `top.v` - Top Level Design
- `fftTop.v` - FFT Top Module
- `FifoBuffer.v` - FIFO Buffer
- `async_fifo.v` - Asynchronous FIFO
- `clock_generator.v` - Clock Generator
- `rtlRam.v` - RTL RAM

#### XSIM Örnekleri
**Konum**: `xsim\systemverilog\dpi\` ve `xsim\verilog\xsi\`

- `simple_export\file.sv` - DPI Export Example
- `simple_import\file.sv` - DPI Import Example
- `counter\counter.v` - Counter Example

#### MIG (Memory Interface Generator) Örnekleri (3 dosya)
**Konum**: `ids_lite\ISE\coregen\ip\xilinx\other\com\xilinx\ip\mig_7series_v1_7\`

- DDR2 SDRAM `example_top.v`
- DDR3 SDRAM `example_top.v`
- QDR II+ SRAM `example_top.v`

**Detaylı Liste**: `vivado_templates_list.txt`

---

### 🔧 VHDL Template ve Örnekler (9 Dosya)
**Kaynak**: `C:\Xilinx\2025.1\Vivado\`

VHDL design template ve örnekleri (example/template içeren dizinlerden)

---

### 🔧 Testbench Dosyaları (4 Dosya)
**Kaynak**: `C:\Xilinx\2025.1\Vivado\data\ip\xilinx\`

SystemVerilog testbench örnekleri:
- ADC/DAC Interface testbenches
- DDR memory testbenches

---

### 🔌 IP Core Örnekleri

#### Toplam IP Core: 597
**Kaynak**: `C:\Xilinx\2025.1\Vivado\data\ip\xilinx\`

#### Örnek İçeren IP Core: 46

##### Connectivity (24 IP)
1. `axi_dma_v7_1` - AXI Direct Memory Access
2. `axi_ethernet_v7_2` - AXI Ethernet MAC
3. `axi_gpio_v2_0` - AXI General Purpose I/O
4. `axi_uartlite_v2_0` - AXI UART Lite
5. `axi_iic_v2_1` - AXI I2C Bus Interface
6. `axi_cdma_v4_1` - AXI Central DMA
7. `ahblite_axi_bridge_v3_0` - AHB-Lite to AXI Bridge
8. `axi_ahblite_bridge_v3_0` - AXI to AHB-Lite Bridge
9. `axi_apb_bridge_v3_0` - AXI to APB Bridge
10. `axi_pcie_v2_9` - AXI PCI Express
... (toplam 24 IP)

##### DSP & Math (1 IP)
1. `vrf_fft_v1_1` - VRF FFT

##### Memory (1 IP)
1. `ddr4_pl_v1_0` - DDR4 Memory Controller
   - `self_refresh_fsm.v`
   - `example_tb_phy.sv`
   - `example_tb_phy_pingpong.sv`
   - `blk_mem_gen_0.sv`

##### Processing (1 IP)
1. `versal_ldpc_v1_0` - Versal LDPC Decoder

##### Other (19 IP)
1. `adc_dac_if_v1_0` - ADC/DAC Interface (4 HDL örneği)
2. `cam_v4_0` - Content Addressable Memory
3. `jesd204c_v4_3` - JESD204C Interface
4. `ldpc_v2_0` - LDPC Encoder/Decoder
5. `polar_v1_1` - Polar Encoder/Decoder
... (toplam 19 IP)

**Detaylı Liste**: `vivado_ip_cores_list.txt`

---

## 3️⃣ DOSYA KAYNAKLARI VE KONUMLARI

### Xilinx Kurulum Dizinleri
```
C:\Xilinx\2025.1\
├── Vivado\
│   ├── examples\
│   │   ├── Vivado_Tutorial\Sources\hdl\
│   │   └── xsim\
│   ├── data\
│   │   └── ip\xilinx\
│   └── ids_lite\ISE\coregen\ip\xilinx\
├── Vitis\
├── data\
│   ├── embeddedsw\
│   ├── ip\xilinx\
│   └── osci_systemc\
└── DocNav\
```

### GitHub FPGA Projeleri
```
C:\Users\murat\Documents\GitHub\
├── VIVADO_DOCS\
├── docs_fpga\
├── ax7010_fpga\
├── z7lite_fpga\
├── z7nano_fpga\
├── coraz7_fpga\
└── nexsys_fpga\
```

---

## 4️⃣ OLUŞTURULAN LİSTE DOSYALARI

RAG eğitimi sırasında oluşturulan detaylı liste dosyaları:

### `ai_assistant/` Dizinindeki Listeler:

1. **`vivado_templates_list.txt`**
   - 118 Verilog/VHDL template ve örnek dosyanın tam listesi
   - Kategorilere ayrılmış (Verilog, VHDL, Testbench)
   - Her dosyanın tam yolu

2. **`vivado_ip_cores_list.txt`**
   - 597 IP Core'un tam listesi
   - Örnek içeren 46 IP'nin detayları
   - Her IP'nin HDL örnek dosyaları

3. **`xilinx_all_pdfs_list.txt`**
   - Xilinx kurulumundaki 26 PDF'in listesi
   - Kategorilere ayrılmış (MIG, IP Docs, Embedded SW, vb.)
   - Her PDF'in tam yolu

4. **`full_training_stats.json`**
   - RAG eğitim istatistikleri
   - Toplam chunk, token, maliyet bilgileri
   - Kaynak bazında dosya dağılımı

---

## 5️⃣ İNDİRİLEBİLİR EK DOKÜMANLAR

IP Core'ların product guide'ları genelde online'dır. İhtiyaç halinde şu kaynaklardan indirilebilir:

### AMD/Xilinx Doküman Portalı
- **Ana Portal**: https://docs.amd.com/
- **IP Product Guides**: https://docs.amd.com/category/ip

### Önemli IP Dokümanları (İndirilebilir)
- **PG021** - AXI DMA
- **PG138** - AXI Ethernet
- **PG144** - AXI GPIO
- **PG142** - AXI UART Lite
- **PG090** - AXI IIC
- **PG065** - Clocking Wizard
- **PG058** - Block Memory Generator
- **PG150** - AXI Interconnect
- **PG247** - SmartConnect

### FPGA Datasheets (İndirilebilir)
- **DS180** - 7-Series FPGAs Overview
- **DS190** - Zynq-7000 SoC Overview
- **DS925** - UltraScale Architecture
- **DS892** - Zynq UltraScale+ MPSoC Overview

---

## 6️⃣ RAG SİSTEMİ İSTATİSTİKLERİ

### Kaynak Bazında Dağılım

| Kaynak | Dosya Sayısı | Chunk Sayısı |
|--------|-------------|--------------|
| Markdown Docs | 88 | 429 |
| Z7Lite Project | 9 | 490 |
| docs_fpga | 5 | 264 |
| AX7010 Project | 9 | 161 |
| Z7Nano Project | 1 | 84 |
| VIVADO_DOCS Workspace | 7 | 21 |
| Xilinx Vivado | 3 | 3 |
| Xilinx Data | 4 | 20 |
| Diğer | 2 | 20 |
| **TOPLAM** | **128** | **1,492** |

### Dosya Tipi Dağılımı

| Tip | Chunk Sayısı |
|-----|-------------|
| PDF | 1,042 |
| Markdown | 450 |
| **TOPLAM** | **1,492** |

---

## 7️⃣ KULLANIM TALİMATLARI

### Mevcut RAG Sistemini Kullanma
```bash
cd ai_assistant
python vivado_agent.py
```

### Yeni Doküman Ekleme
1. PDF/Markdown dosyalarını ilgili klasöre kopyalayın:
   - `official_docs/IP_Cores/` - IP Core dokümanları
   - `official_docs/Design_Tools/` - Vivado/Vitis kılavuzları
   - `official_docs/Datasheets/` - FPGA datasheetleri

2. RAG'i yeniden eğitin:
```bash
python train_rag_full_system.py
```

### Template/Örnekleri RAG'e Ekleme
Verilog/VHDL template'lerini eklemek için `train_rag_full_system.py` zaten yapılandırılmıştır, sadece çalıştırın.

---

## 8️⃣ NOTLAR

- ✅ RAG sistemi aktif ve çalışıyor
- ✅ 128 dosya başarıyla işlendi
- ⏳ 118 Verilog/VHDL template hazır, eklenmesi bekleniyor
- ⏳ 46 IP Core örneği hazır, eklenmesi bekleniyor
- 💡 Online IP dokümanları manuel olarak indirilebilir

---

**Son Güncelleme**: 18 Ocak 2026
**RAG Database**: `vivado_vectordb_full/`
**Collection**: `vivado_full_system` (1,492 döküman)
