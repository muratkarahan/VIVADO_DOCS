# Virtex-7 GTY to DDR4 via AXI DMA - Tam Tasarım

Bu proje, Virtex-7 FPGA üzerinde GTY transceiver'dan gelen yüksek hızlı seriyi AXI DMA Stream kullanarak DDR4 belleğe yazan tam bir donanım tasarımıdır.

## 📋 İçerik

```
virtex7_gty_dma_ddr4/
├── README.md                    # Bu dosya
├── create_project.tcl           # Vivado proje oluşturma scripti
├── gty_to_axis_bridge.v        # GTY RX -> AXI-Stream bridge modülü
├── dma_control.c                # MicroBlaze kontrol yazılımı
└── constraints.xdc              # Pin atamaları ve timing constraints
```

## 🎯 Tasarım Özeti

### Veri Akış Yolu
```
GTY RX → AXI-Stream Bridge → AXIS FIFO → AXI DMA (S2MM) → DDR4 Memory
```

### Donanım Bileşenleri

1. **GTY Transceiver** - 10G seri veri alıcı
   - 64-bit user data genişliği
   - 156.25 MHz user clock
   - 64B/66B encoding

2. **AXI-Stream Bridge** - Özel Verilog modülü
   - GTY RX data → AXI4-Stream dönüşümü
   - Paket oluşturma (TLAST sinyali)
   - Flow control (TREADY/TVALID)

3. **AXIS Data FIFO** - Clock domain crossing
   - 16K derinlik
   - Async FIFO (GTY 156.25MHz → AXI 100MHz)
   - Back-pressure yönetimi

4. **AXI DMA** - Stream to Memory Map
   - S2MM (Stream to Memory Mapped) modu
   - 512-bit DDR4 veri yolu
   - Burst transfer (256 beat)

5. **DDR4 Controller** - Xilinx MIG IP
   - 64-bit data width
   - AXI4 interface
   - 2400 MT/s (1200 MHz)

6. **MicroBlaze** - Kontrol işlemcisi
   - DMA programlama
   - Transfer yönetimi
   - Monitoring

## 🚀 Kurulum ve Kullanım

### 1. Proje Oluşturma

Vivado'yu açın ve TCL console'dan:

```tcl
cd C:/Users/murat/Documents/GitHub/VIVADO_DOCS/virtex7_gty_dma_ddr4
source create_project.tcl
```

### 2. Donanım Özelleştirme

#### Board'a Göre Değiştirilmesi Gerekenler:

**a) FPGA Part:**
- `create_project.tcl` dosyasında `part_name` değişkenini değiştirin
- Örnek: `xc7vx485tffg1761-2` → sizin board'unuzun part numarası

**b) Pin Atamaları:**
- `constraints.xdc` dosyasındaki tüm pin numaralarını board'unuza göre güncelleyin
- Özellikle:
  - GTY RX/TX pinleri
  - System clock pinleri  
  - DDR4 pinleri (MIG wizard'dan alınabilir)
  - UART ve GPIO pinleri

**c) GTY Konfigürasyonu:**
- Block Design'da GTY Wizard'ı açın
- Line rate, encoding, protocol ayarlarını yapın
- RefClk frekansını board'unuza göre ayarlayın

**d) DDR4 Konfigürasyonu:**
- MIG wizard'ı açın
- Board'unuzdaki DDR4 chip'e göre ayarlayın
- Pin assignment'ı MIG'den export edin

### 3. Synthesis ve Implementation

```tcl
# Vivado GUI veya TCL:
launch_runs synth_1 -jobs 8
wait_on_run synth_1

launch_runs impl_1 -jobs 8
wait_on_run impl_1

launch_runs impl_1 -to_step write_bitstream -jobs 8
wait_on_run impl_1
```

### 4. Yazılım Geliştirme

#### a) Vitis IDE ile:

1. Hardware platform export et:
   ```tcl
   write_hw_platform -fixed -include_bit -force -file ./gty_dma_system.xsa
   ```

2. Vitis'te yeni platform projesi oluştur
3. `dma_control.c` dosyasını application project'e ekle
4. BSP'de `xaxidma` ve `xgpio` driver'larını enable et
5. Build ve debug

#### b) SDK ile (Vivado 2019.2 ve öncesi):

1. File → Export → Export Hardware
2. File → Launch SDK
3. File → New → Application Project
4. `dma_control.c` dosyasını src/ klasörüne kopyala
5. BSP settings'de driver'ları ekle

### 5. Test ve Debug

#### Hardware Debug:

```tcl
# ILA (Integrated Logic Analyzer) ekle:
- GTY RX data bus
- AXIS FIFO interface
- AXI DMA S2MM interface
- DDR4 write interface
```

#### Software Debug:

1. UART üzerinden MicroBlaze'e bağlan (115200 baud)
2. Program çalıştır
3. Transfer istatistiklerini izle:
   ```
   >>> Transfer #100 tamamlandı | Adres: 0x80100000 | Toplam: 100 MB
   ```

## 📊 Performans

### Teorik Maksimum:
- **GTY Line Rate:** 10.3125 Gb/s
- **Effective Data Rate:** ~9.7 Gb/s (64B/66B overhead)
- **DDR4 Bandwidth:** 38.4 GB/s (read+write combined)
- **AXI DMA Throughput:** ~6.4 GB/s (512-bit @ 100MHz)

### Beklenen Performans:
- **Sustained Throughput:** 800-1000 MB/s
- **Burst Throughput:** 1.2 GB/s
- **Latency:** <100 μs (first byte)

### Performans Optimizasyonu:

1. **AXI DMA Burst Size:** 256'ya çıkarın
2. **DDR4 Frequency:** 2400 MT/s → 2666 MT/s
3. **AXIS FIFO Depth:** 16K → 32K (daha fazla buffering)
4. **AXI SmartConnect:** Routing optimize edin

## 🔧 Sorun Giderme

### GTY Lock Alamıyor:
- RefClk frekansını kontrol edin
- RX equalizer ayarlarını optimize edin
- Loopback modunda test edin

### DMA Transfer Başlamıyor:
- S_AXIS_S2MM sinyallerini ILA ile kontrol edin
- TVALID, TREADY handshake'i doğrulayın
- DDR4 controller'ın init_calib_complete sinyalini kontrol edin

### Veri Bütünlüğü Hatası:
- Cache coherency kontrol edin (flush/invalidate)
- AXI SmartConnect QoS ayarlarını kontrol edin
- Timing violation var mı kontrol edin (timing report)

## 📚 Referanslar

### Xilinx Dokümanları:
- **UG471** - 7 Series FPGAs SelectIO Resources
- **UG476** - 7 Series FPGAs GTX/GTH Transceivers
- **PG021** - AXI DMA LogiCORE IP Product Guide
- **PG022** - AXI4-Stream Infrastructure IP Product Guide
- **PG150** - DDR4 Memory Interface Solution

### Örnek Tasarımlar:
```
vivado-examples/Vivado-Design-Tutorials-2025.2/UltraScalePlus/DFX/
vivado-examples/Vivado-Design-Tutorials-2025.2/Versal/Memory_and_NoC/
```

## 💡 Geliştirme Önerileri

### 1. Multi-Channel GTY:
- 4 kanal GTY → 4x AXI DMA → DDR4
- Total bandwidth: ~4 GB/s

### 2. DMA Interrupt Kullanımı:
- Polling yerine interrupt
- CPU overhead azaltma

### 3. Scatter-Gather DMA:
- Ring buffer yönetimi
- Otomatik buffer switching

### 4. High-Level Synthesis (HLS):
- Data processing pipeline ekleme
- GTY ile DMA arası ön işleme

### 5. NoC Integration (Versal):
- AXI NoC ile bandwidth artışı
- Multi-master support

## 📞 Destek

Bu tasarım RAG sistemi üzerinden oluşturulmuştur. Sorularınız için:
- Vivado Agent'ı kullanın: `python vivado_agent.py`
- Xilinx documentation arşivine bakın

## 📄 Lisans

Bu örnek tasarım eğitim amaçlıdır. Xilinx IP'leri için geçerli lisans koşulları geçerlidir.

---

**Son Güncelleme:** 18 Ocak 2026
**Vivado Versiyonu:** 2025.2
**Hedef FPGA:** Virtex-7 (VC707, VCU108, vb.)
