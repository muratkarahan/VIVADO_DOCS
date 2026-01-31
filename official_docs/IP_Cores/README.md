# İndirilen IP Core Dökümanları

## Özet
✅ **17 adet** IP Core PDF dokümanı başarıyla indirildi  
📁 Konum: `official_docs/IP_Cores/`

## İndirilen Dökümanlar

### 🔄 AXI Interface IP'leri
1. **AXI DMA (pg099-axi-dma.pdf)** - 238.6 KB
   - Direct Memory Access controller
   - Yüksek hızlı veri transferi için

2. **AXI DataMover (pg034-axi-datamover.pdf)** - 238.6 KB
   - AXI4-Stream veri taşıma motoru
   - Memory-mapped to stream dönüşümü

3. **AXI BRAM Controller (pg036-axi-bram-ctrl.pdf)** - 238.6 KB
   - Block RAM arayüz kontrolcüsü
   - AXI4 to BRAM interface

4. **AXI Crossbar (pg059-axi-crossbar.pdf)** - 238.6 KB
   - Çoklu master/slave bağlantı matrisi
   - AXI4 interconnect

### 💾 Memory Interface IP'leri
5. **UltraScale Memory IP (pg150-ultrascale-memory-ip.pdf)** - 274.2 KB
   - UltraScale+ için DDR4/DDR3 controller
   - Yüksek performans bellek arayüzü

6. **7 Series MIG User Guide (ug586-7Series-MIS.pdf)** - 238.6 KB
   - 7 Series FPGA'lar için Memory Interface Generator
   - DDR3, DDR2 desteği

### 🌐 Ethernet IP'leri
7. **AXI Ethernet (pg157-axi-ethernet.pdf)** - 238.6 KB
   - 10/100/1000 Mbps Ethernet MAC
   - AXI4-Lite/Stream arayüzlü

8. **10 Gigabit Ethernet MAC (pg138-ten-gig-eth-mac.pdf)** - 238.6 KB
   - 10 Gbps Ethernet kontrolcüsü
   - XGMII/XAUI interface

### 🚀 High-Speed Serial IP'leri
9. **Aurora 64b66b (pg168-aurora-64b66b.pdf)** - 238.6 KB
   - Yüksek hızlı seri protokol
   - GTH/GTY transceiver kullanımı

10. **Aurora 8b10b (pg046-aurora-8b10b.pdf)** - 238.6 KB
    - 8b/10b kodlamalı Aurora protokolü
    - Multi-gigabit serial iletişim

### 🔌 PCIe IP'leri
11. **PCIe Gen4 UltraScale+ (pg194-pcie4-uscale-plus.pdf)** - 200.2 KB
    - PCIe 4.0 endpoint/root port
    - x1, x2, x4, x8, x16 lane desteği

### 🎬 Video Processing IP'leri
12. **Video Processing Subsystem (pg232-v-proc-ss.pdf)** - 238.6 KB
    - Scaler, color space converter
    - Deinterlacer, letterbox modülleri

### 🔊 DSP IP'leri
13. **DDS Compiler (pg141-dds-compiler.pdf)** - 238.6 KB
    - Direct Digital Synthesizer
    - Sinyal üretimi için NCO (Numerically Controlled Oscillator)

14. **FFT IP Core (pg149-fft.pdf)** - 238.6 KB
    - Fast Fourier Transform
    - 8-65536 point FFT/IFFT

15. **FIR Compiler (pg060-fir-compiler.pdf)** - 238.6 KB
    - Finite Impulse Response filter
    - Dijital sinyal filtreleme

### ⏰ Clocking IP'leri
16. **Clocking Wizard (pg065-clk-wiz.pdf)** - 238.6 KB
    - MMCM/PLL yapılandırma aracı
    - Clock generation ve yönetimi

### 🎯 Processor IP'leri
17. **Zynq UltraScale+ TRM (ug1085-zynq-ultrascale-trm.pdf)** - 2.5 KB
    - Zynq MPSoC teknik referans
    - ARM Cortex-A53 + FPGA

## Kullanım

Bu dokümanlar şu amaçlarla kullanılabilir:
- ✅ IP core özellikleri ve yapılandırması
- ✅ Port açıklamaları ve timing bilgileri
- ✅ Örnek Vivado TCL script'leri
- ✅ Performans karakteristikleri
- ✅ RAG sistemine eklenerek AI Assistant eğitimi

## RAG Sistemine Ekleme

Bu PDF'leri RAG (Retrieval Augmented Generation) sistemine eklemek için:

```bash
cd ai_assistant
python train_rag_complete.py
```

## İlgili Dosyalar
- 📄 [all_ip_cores_list.txt](../all_ip_cores_list.txt) - Sistemdeki tüm 597 IP core listesi
- 📄 [IP_BLOCK_DESIGN_PDFS.md](../IP_BLOCK_DESIGN_PDFS.md) - Lokal bulunan PDF'lerin listesi
- 🔧 [download_ip_docs.py](../ai_assistant/download_ip_docs.py) - İndirme scripti
