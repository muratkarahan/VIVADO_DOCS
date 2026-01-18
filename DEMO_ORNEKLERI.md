# 🎯 Vivado FPGA Expert - Demo Kullanım Örnekleri

Bu dosyada VS Code Chat'te `@vivado` ile kullanabileceğiniz demo sorguları bulunuyor.

---

## 🚀 DEMO 1: Temel Sorular

### AXI Protokolü
```
@vivado AXI4-Lite nedir ve AXI4 Full'dan farkı nedir?
```

**Beklenen Cevap:**
- AXI4-Lite açıklaması (basitleştirilmiş, tek transfer)
- AXI4 Full ile karşılaştırma (burst desteği)
- Kullanım senaryoları (register access vs DMA)
- Kaynak: PG057, UG1037

---

### Zynq PS-PL İletişimi
```
@vivado Zynq Processing System ile Programmable Logic arasında veri aktarımı nasıl yapılır?
```

**Beklenen Cevap:**
- AXI GP/HP/ACP portları
- AXI DMA kullanımı
- Interrupt yapısı
- Linux driver yazımı
- Kaynak: UG585, PG080

---

### Clock Management
```
@vivado MMCM ve PLL arasındaki farklar nelerdir?
```

**Beklenen Cevap:**
- MMCM özellikleri (mixed-mode clock manager)
- PLL özellikleri (phase-locked loop)
- Jitter performance
- Kullanım senaryoları
- Kaynak: UG472, PG065

---

## 🔍 DEMO 2: Döküman Arama (/search)

### FIFO Generator
```
@vivado /search FIFO generator IP configuration
```

**Beklenen Sonuç:**
- PG058 → FIFO Generator User Guide
- Independent/common clock mode
- Read/write width configuration
- Full/empty flag usage
- 3-5 ilgili döküman bölümü

---

### Timing Constraints
```
@vivado /search XDC timing constraints
```

**Beklenen Sonuç:**
- UG903 → Using Constraints
- create_clock, create_generated_clock
- set_input_delay, set_output_delay
- set_false_path, set_multicycle_path
- Constraint priority

---

### IP Integrator
```
@vivado /search IP Integrator block design automation
```

**Beklenen Sonuç:**
- UG994 → IP Integrator User Guide
- Block design creation
- Connection automation
- Address editor
- Validate design

---

## 💻 DEMO 3: Kod Örnekleri (/code)

### AXI4-Stream FIFO (Verilog)
```
@vivado /code AXI4-Stream FIFO interface verilog
```

**Beklenen Kod:**
```verilog
module axis_fifo #(
    parameter DATA_WIDTH = 32,
    parameter DEPTH = 16
)(
    input wire aclk,
    input wire aresetn,
    
    // AXI4-Stream Slave (Input)
    input  wire [DATA_WIDTH-1:0] s_axis_tdata,
    input  wire                  s_axis_tvalid,
    output wire                  s_axis_tready,
    input  wire                  s_axis_tlast,
    
    // AXI4-Stream Master (Output)
    output wire [DATA_WIDTH-1:0] m_axis_tdata,
    output wire                  m_axis_tvalid,
    input  wire                  m_axis_tready,
    output wire                  m_axis_tlast
);
// ... (tam kod örneği)
```

---

### Zynq Bare-Metal Driver (C)
```
@vivado /code Zynq GPIO bare-metal driver C
```

**Beklenen Kod:**
```c
#include "xgpiops.h"
#include "xparameters.h"

XGpioPs Gpio;

int gpio_init(void) {
    XGpioPs_Config *ConfigPtr;
    int Status;
    
    ConfigPtr = XGpioPs_LookupConfig(XPAR_PS7_GPIO_0_DEVICE_ID);
    if (ConfigPtr == NULL) {
        return XST_FAILURE;
    }
    
    Status = XGpioPs_CfgInitialize(&Gpio, ConfigPtr, ConfigPtr->BaseAddr);
    if (Status != XST_SUCCESS) {
        return XST_FAILURE;
    }
    
    // Configure as output
    XGpioPs_SetDirectionPin(&Gpio, 54, 1);
    XGpioPs_SetOutputEnablePin(&Gpio, 54, 1);
    
    return XST_SUCCESS;
}

void gpio_write(u32 pin, u32 value) {
    XGpioPs_WritePin(&Gpio, pin, value);
}
```

---

### Vivado TCL Build Script
```
@vivado /code Vivado project TCL build script
```

**Beklenen Kod:**
```tcl
# Vivado TCL Build Script
# Create project
create_project my_project ./my_project -part xc7z020clg400-1

# Set properties
set_property board_part xilinx.com:zc702:part0:1.4 [current_project]
set_property target_language Verilog [current_project]

# Add source files
add_files {./src/rtl/top.v ./src/rtl/controller.v}
add_files -fileset constrs_1 {./constraints/timing.xdc ./constraints/pinout.xdc}

# Create block design
create_bd_design "system"
source ./scripts/bd_system.tcl

# Generate wrapper
make_wrapper -files [get_files system.bd] -top
add_files -norecurse ./my_project/my_project.srcs/sources_1/bd/system/hdl/system_wrapper.v

# Synthesis
launch_runs synth_1 -jobs 8
wait_on_run synth_1

# Implementation
launch_runs impl_1 -to_step write_bitstream -jobs 8
wait_on_run impl_1

# Export hardware
write_hw_platform -fixed -include_bit -force -file ./my_project.xsa
```

---

## 📚 DEMO 4: Kavram Açıklamaları (/explain)

### IP Integrator
```
@vivado /explain IP Integrator block design workflow
```

**Beklenen Açıklama:**
- IP Integrator nedir?
- Block design creation
- IP catalog ve customization
- Connection automation
- Address editor
- Validate design
- Generate output products
- Kaynak: UG994

---

### AXI Interconnect
```
@vivado /explain AXI Interconnect IP
```

**Beklenen Açıklama:**
- AXI Interconnect mimarisi
- Master/slave interface configuration
- Arbiter modes (round-robin, fixed priority)
- Address decoding
- Data width conversion
- Protocol conversion
- Kaynak: PG057

---

### Timing Closure
```
@vivado /explain timing closure methodology
```

**Beklenen Açıklama:**
- Timing analysis temelleri
- Setup/hold time violations
- Critical path optimization
- Pipelining techniques
- Floorplanning
- Physical optimization
- Kaynak: UG949, UG906

---

## 🎨 DEMO 5: Karmaşık Senaryolar

### Zynq Linux Sistemi
```
@vivado Zynq üzerinde custom IP ile Linux driver nasıl yazılır?
```

**Beklenen Cevap:**
- Custom IP tasarımı (AXI4-Lite slave)
- Device tree overlay
- Platform device driver
- Character device interface
- User space application
- Kaynak: UG585, UG1144

---

### High-Speed Interface
```
@vivado GTH transceiver ile 10G Ethernet nasıl yapılır?
```

**Beklenen Cevap:**
- GTH configuration (line rate, ref clock)
- 10G Ethernet MAC IP setup
- Aurora protocol alternative
- Eye scan ve debugging
- Timing constraints
- Kaynak: UG576, PG157

---

### Vitis HLS Optimizasyonu
```
@vivado Vitis HLS ile C kodunu nasıl optimize ederim?
```

**Beklenen Cevap:**
- Pipeline directive
- Unroll directive
- Array partitioning
- Dataflow optimization
- Interface synthesis (AXI4-Stream)
- Resource vs latency trade-off
- Kaynak: UG1399

---

## 🧪 Nasıl Test Edilir?

### 1️⃣ VS Code Extension ile (ÖNERİLEN)
```
1. VS Code'da VIVADO_DOCS.code-workspace'i aç
2. Run > Start Debugging (F5)
3. Extension Development Host açılır
4. Chat'i aç (Ctrl+Shift+I)
5. Yukarıdaki demo'lardan birini kopyala-yapıştır
```

### 2️⃣ Terminal Demo ile
```powershell
cd C:\Users\murat\Documents\GitHub\VIVADO_DOCS\ai_assistant
python demo.py
```

### 3️⃣ Manuel Agent ile
```powershell
cd C:\Users\murat\Documents\GitHub\VIVADO_DOCS\ai_assistant
python vivado_agent.py
# Menüden "1" seçin (Chat modu)
```

---

## 📊 Her Demo Gösterecek:

✅ **Semantik Arama** - ChromaDB'den ilgili dökümanlar
✅ **RAG Pipeline** - Context injection + GPT-4
✅ **Kaynak Takibi** - Hangi UG/PG kullanıldı
✅ **Token Maliyeti** - Her sorgu için maliyet
✅ **Kod Formatı** - Syntax highlighting ile kod blokları
✅ **Türkçe Açıklama** - Teknik terimler İngilizce

---

## 🎯 Demo Başarı Kriterleri

| Kriter | Başarılı ✅ | Başarısız ❌ |
|--------|------------|-------------|
| Cevap süresi | < 5 saniye | > 10 saniye |
| Kaynak bulma | 3+ döküman | 0 döküman |
| Kod formatı | Syntax valid | Hatalı kod |
| Türkçe kalitesi | Akıcı | Kötü çeviri |
| Token kullanımı | < 3000 | > 5000 |

---

## 💡 İpuçları

1. **Spesifik olun:** "AXI nedir?" yerine "AXI4-Lite master interface nasıl oluşturulur?"
2. **Komutları kullanın:** `/search`, `/code`, `/explain` daha iyi sonuç verir
3. **Dil belirtin:** Kod örneklerinde "Verilog", "VHDL", "TCL" veya "C" ekleyin
4. **Bağlam verin:** "Zynq-7020 için" veya "UltraScale+ ile" gibi detaylar ekleyin
5. **Versiyon belirtin:** "Vivado 2023.2" gibi versiyon bilgisi yararlıdır

---

## 🔧 Vivado Workflow'a Özgü Örnekler

### Block Design Otomasyon
```
@vivado IP Integrator'da Zynq PS + AXI GPIO sistemi nasıl oluşturulur?
```

### Constraint Yazımı
```
@vivado /code XDC constraints for DDR3 interface
```

### Simulation
```
@vivado XSIM ile testbench nasıl çalıştırılır?
```

### Debugging
```
@vivado ILA (Integrated Logic Analyzer) nasıl eklenir?
```

---

🚀 **Şimdi deneyin! Extension'ı başlatın ve demo'ları test edin!**
