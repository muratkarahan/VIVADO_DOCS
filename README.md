# 🚀 VIVADO_DOCS - Xilinx Vivado FPGA AI Assistant

**Xilinx Vivado Design Suite için AI destekli döküman arama ve kod asistanı**

[![VS Code](https://img.shields.io/badge/VS%20Code-Extension-blue)](https://code.visualstudio.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange)](https://openai.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-purple)](https://www.trychroma.com/)

---

## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Proje Yapısı](#proje-yapısı)
- [Dökümanlar](#dökümanlar)

---

## 🎯 Proje Hakkında

VIVADO_DOCS, Xilinx Vivado Design Suite kullanıcıları için geliştirilmiş **RAG (Retrieval-Augmented Generation)** tabanlı bir AI asistanıdır. 

### Ne yapar?

- 📚 **Vivado dökümanlarında semantik arama** - ChromaDB vektör database
- 💬 **GPT-4 ile akıllı soru-cevap** - Context-aware yanıtlar
- 💻 **Verilog/VHDL/TCL kod örnekleri** - Best practices ile
- 🔍 **VS Code entegrasyonu** - @vivado komutlarıyla chat üzerinden
- 🤖 **MCP Server desteği** - Model Context Protocol

### Kimler için?

- Xilinx FPGA geliştiricileri
- Vivado Design Suite kullanan mühendisler
- Zynq/UltraScale+ SoC tasarımcıları
- FPGA öğrencileri ve eğitmenler

---

## ✨ Özellikler

### 1️⃣ RAG Pipeline

```
Kullanıcı Sorusu → ChromaDB Arama → İlgili Dökümanlar → GPT-4 → Yanıt + Kaynaklar
```

- **Semantik Arama:** OpenAI embeddings ile akıllı döküman eşleştirme
- **Context Injection:** İlgili döküman bölümleri GPT-4'e beslenir
- **Kaynak Takibi:** Her yanıtta hangi PDF/sayfa kullanıldığı gösterilir
- **Çoklu Format:** Verilog, VHDL, TCL, SystemVerilog, C/C++

### 2️⃣ VS Code Extension

```bash
@vivado AXI4-Stream interface nasıl kullanılır?
@vivado /search UltraScale+ clock manager
@vivado /code FIFO generator TCL script
```

- **Chat Entegrasyonu:** VS Code Chat panel üzerinden
- **Komut Desteği:** `/search`, `/code`, `/explain`
- **Syntax Highlighting:** Kod blokları formatlanmış
- **Hızlı Erişim:** Ctrl+Shift+I ile chat açılır

### 3️⃣ MCP Server

Model Context Protocol ile standardize edilmiş AI etkileşimi:

- `vivado_search` - Döküman arama
- `vivado_code` - Kod örneği
- `vivado_explain` - Kavram açıklama
- `vivado_debug` - Hata ayıklama yardımı

### 4️⃣ Kapsanan Konular

#### 📘 Vivado Design Suite
- IP Integrator (Block Design)
- Synthesis & Implementation
- Timing Analysis
- Constraints (XDC)
- Simulation (XSIM)
- TCL scripting

#### 🔌 IP Cores
- AXI4/AXI4-Lite/AXI4-Stream
- FIFO Generator
- Clock Manager (MMCM/PLL)
- Block Memory Generator
- DMA Controller
- Gigabit Transceivers (GTH/GTY)

#### 💻 Embedded Systems
- Zynq-7000 SoC
- Zynq UltraScale+ MPSoC
- MicroBlaze
- Vitis Software Platform

#### 🎨 High-Level Synthesis
- Vitis HLS
- C/C++ to RTL
- Optimization directives

---

## 🛠️ Kurulum

### Ön Gereksinimler

- **Python 3.8+**
- **VS Code 1.80+**
- **OpenAI API Key** ([alın](https://platform.openai.com/api-keys))
- **Git**

### 1️⃣ Repository'yi Klonlayın

```powershell
cd C:\Users\<username>\Documents\GitHub
git clone <VIVADO_DOCS_REPO_URL>
cd VIVADO_DOCS
```

### 2️⃣ Python Ortamını Hazırlayın

```powershell
# Virtual environment oluştur
python -m venv venv

# Aktive et (Windows)
.\venv\Scripts\Activate.ps1

# Paketleri yükle
pip install -r ai_assistant/requirements.txt
```

### 3️⃣ OpenAI API Key Ayarlayın

```powershell
# Ortam değişkeni olarak (Windows)
$env:OPENAI_API_KEY = "sk-proj-..."

# veya .env dosyası oluştur
echo OPENAI_API_KEY=sk-proj-... > .env
```

### 4️⃣ VS Code Extension'ı Yükleyin

```powershell
cd ai_assistant/vscode-extension
npm install
npm run compile
```

VS Code'da **F5** ile Extension Development Host'u başlatın.

### 5️⃣ Dökümanları İndirin ve Indexleyin

```powershell
# official_docs klasörüne Vivado PDF'leri yerleştirin
# Örnek: UG902, UG912, UG949, vb.

# Indexleme yapın
python ai_assistant/setup_vivado_ai.py
```

---

## 🚀 Kullanım

### Yöntem 1: VS Code Extension (ÖNERİLEN)

1. **Workspace'i aç:** `VIVADO_DOCS.code-workspace`
2. **Extension'ı başlat:** `F5` (Debug mode)
3. **Chat'i aç:** `Ctrl+Shift+I`
4. **Sorular sorun:**

```
@vivado AXI4-Lite master interface nasıl oluşturulur?
@vivado /search Zynq clock configuration
@vivado /code FIFO verilog
@vivado /explain MMCM phase shift
```

### Yöntem 2: Terminal Demo

```powershell
cd ai_assistant
python demo.py

# Demo menüsünden seçim yapın:
# 1. Semantik Arama Testi
# 2. RAG Pipeline Testi  
# 3. Kod Örneği Testi
```

### Yöntem 3: Python Agent

```powershell
cd ai_assistant
python vivado_agent.py

# Interaktif chat modu
# Sorularınızı yazın, AI yanıtlar
```

### Yöntem 4: MCP Server

```powershell
cd ai_assistant
python vivado_mcp_server.py

# MCP protocol ile haberleşme
# Claude Desktop, VS Code vb. istemcilerle
```

---

## 📁 Proje Yapısı

```
VIVADO_DOCS/
│
├── README.md                          # Bu dosya
├── VIVADO_DOCS.code-workspace         # VS Code workspace
├── DEMO_ORNEKLERI.md                  # Demo kullanım senaryoları
├── KOD_ORNEKLERI.md                   # Kod örnekleri (Verilog/VHDL/TCL)
├── EGITIM_PLANI.md                    # Vivado öğrenme yol haritası
├── OFFICIAL_DOCS_INDEX.md             # Döküman kataloğu
│
├── ai_assistant/                      # AI altyapısı
│   ├── vivado_agent.py                # Ana RAG agent
│   ├── vivado_mcp_server.py           # MCP server
│   ├── setup_vivado_ai.py             # Döküman indexleme
│   ├── demo.py                        # Test script'leri
│   ├── requirements.txt               # Python bağımlılıkları
│   ├── MCP_SERVER_KURULUM.md          # MCP kurulum rehberi
│   ├── vivado_vectordb/               # ChromaDB vektör database
│   └── vscode-extension/              # VS Code eklentisi
│       ├── package.json
│       ├── src/
│       └── resources/
│
├── official_docs/                     # Xilinx resmi dökümanları
│   ├── README.md
│   ├── DOSYA_LISTESI.txt
│   ├── Design_Tools/                  # Vivado/Vitis UG'ler
│   ├── IP_Cores/                      # IP datasheet'leri
│   ├── SoC_Embedded/                  # Zynq/UltraScale+ docs
│   ├── Transceivers/                  # GTH/GTY guides
│   └── Datasheets/                    # FPGA datasheets
│
├── code_examples/                     # Kod örnekleri
│   ├── verilog/
│   ├── vhdl/
│   ├── tcl/
│   └── hls/
│
└── vivado-examples/                   # Örnek projeler
    ├── axi_dma_example/
    ├── zynq_minimal_design/
    └── ultrascale_clock_example/
```

---

## 📚 Dökümanlar

### İndirmeniz Gereken PDF'ler

Xilinx [Documentation Portal](https://www.xilinx.com/support/documentation.html) üzerinden:

#### 🔧 Vivado Design Suite
- **UG835** - Vivado Design Suite Tcl Command Reference
- **UG912** - Vivado Design Suite Properties Reference
- **UG949** - UltraFast Design Methodology Guide
- **UG906** - Vivado Design Suite User Guide: Design Analysis and Closure
- **UG904** - Vivado Design Suite User Guide: Implementation

#### 🔌 IP Cores
- **PG057** - AXI Interconnect
- **PG058** - FIFO Generator
- **PG065** - Block Memory Generator
- **PG080** - AXI DMA
- **PG094** - XADC Wizard

#### 💻 Zynq/UltraScale+
- **UG585** - Zynq-7000 SoC Technical Reference Manual
- **UG1085** - Zynq UltraScale+ MPSoC Technical Reference Manual
- **UG1144** - PetaLinux Tools Documentation Reference Guide

#### 🎨 Vitis HLS
- **UG1399** - Vitis HLS User Guide
- **UG1393** - Vitis Unified Software Platform Documentation

**Not:** PDF'leri `official_docs/` altındaki ilgili klasörlere yerleştirin.

---

## 💡 Demo Senaryoları

### 1. AXI4 Interface Oluşturma

```
@vivado AXI4-Lite slave nasıl oluşturulur?
```

**Cevap içerir:**
- IP Integrator adımları
- Verilog kod örneği
- TCL scripting
- Kaynak: PG057, UG994

### 2. Zynq PS-PL Bağlantısı

```
@vivado Zynq PS ile PL fabric arasında veri aktarımı nasıl yapılır?
```

**Cevap içerir:**
- AXI GP/HP portları
- DMA kullanımı
- Linux driver'ı
- Kaynak: UG585, UG1085

### 3. Timing Constraint

```
@vivado /code XDC timing constraints
```

**Döner:**
```tcl
# Clock tanımlamaları
create_clock -period 10.000 -name clk100 [get_ports clk]
create_generated_clock -name clk200 -source [get_ports clk] \\
    -multiply_by 2 [get_pins MMCM_inst/CLKOUT0]

# I/O gecikmeleri
set_input_delay -clock clk100 -max 3.000 [get_ports data_in]
set_output_delay -clock clk100 -max 2.000 [get_ports data_out]

# False path
set_false_path -from [get_clocks clk100] -to [get_clocks clk200]
```

### 4. FIFO Generator

```
@vivado FIFO generator IP nasıl yapılandırılır?
```

**Cevap içerir:**
- IP Integrator configurator
- Read/write interface
- Full/empty flags
- Kaynak: PG057

---

## 🔧 Geliştirme

### Extension'ı Debug Etme

```powershell
cd ai_assistant/vscode-extension
code .
# F5 ile debug başlat
```

### Test Çalıştırma

```powershell
# Unit testler
pytest ai_assistant/tests/

# Integration test
python ai_assistant/demo.py
```

### Döküman Yeniden İndexleme

```powershell
# Yeni PDF ekledikten sonra
python ai_assistant/setup_vivado_ai.py --reindex
```

---

## 📊 Performans

| Metrik | Değer |
|--------|-------|
| Ortalama cevap süresi | < 3 saniye |
| Döküman bulma doğruluğu | ~90% |
| Kod syntax doğruluğu | ~95% |
| Token kullanımı/sorgu | ~2500 |

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Commit yapın (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/YeniOzellik`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır.

**Not:** Xilinx Vivado dökümanları Xilinx/AMD'nin telif hakkıdır. Bu proje yalnızca arama ve referans amaçlıdır.

---

## 🙏 Teşekkürler

- **OpenAI** - GPT-4 API
- **ChromaDB** - Vektör database
- **Xilinx/AMD** - Vivado Design Suite dökümanları
- **VS Code Team** - Extension API

---

## 📞 İletişim

Sorularınız için:
- **Issues** - GitHub Issues kullanın
- **Discussions** - Topluluk forumu

---

## 🎓 Öğrenme Kaynakları

- [EGITIM_PLANI.md](EGITIM_PLANI.md) - Adım adım Vivado öğrenme
- [DEMO_ORNEKLERI.md](DEMO_ORNEKLERI.md) - Hazır demo sorguları
- [KOD_ORNEKLERI.md](KOD_ORNEKLERI.md) - Verilog/VHDL/TCL kodu

---

🚀 **Şimdi başlayın! Extension'ı debug modda çalıştırın ve @vivado ile sorularınızı sorun!**
