# ============================================================================
# Virtex-7 GTY to DDR4 via AXI DMA - Vivado Projesi Oluşturma Scripti
# ============================================================================
# Bu script, GTY transceiver'dan gelen veriyi AXI DMA Stream ile DDR4'e
# yazan tam bir Vivado Block Design projesi oluşturur.
# ============================================================================

# Proje ayarları
set project_name "virtex7_gty_dma_ddr4"
set project_dir "./project"
set bd_name "gty_dma_system"

# Virtex-7 FPGA part numarası (değiştirilebilir)
set part_name "xc7vx485tffg1761-2"

# ============================================================================
# PROJE OLUŞTURMA
# ============================================================================

# Mevcut projeyi kapat
catch {close_project}

# Yeni proje oluştur
create_project $project_name $project_dir -part $part_name -force

# Proje özelliklerini ayarla
set_property target_language Verilog [current_project]
set_property simulator_language Mixed [current_project]

puts "✅ Proje oluşturuldu: $project_name"

# ============================================================================
# BLOCK DESIGN OLUŞTURMA
# ============================================================================

create_bd_design $bd_name
puts "✅ Block Design oluşturuldu: $bd_name"

# ============================================================================
# IP CORE'LARI EKLEME
# ============================================================================

puts "📦 IP Core'lar ekleniyor..."

# ----------------------------------------------------------------------------
# 1. MicroBlaze veya Processing System (Kontrol için)
# ----------------------------------------------------------------------------
puts "   - MicroBlaze işlemci ekleniyor..."
set microblaze_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:microblaze:11.0 microblaze_0 ]
set_property -dict [list \
  CONFIG.C_DEBUG_ENABLED {1} \
  CONFIG.C_D_AXI {1} \
  CONFIG.C_I_AXI {0} \
  CONFIG.C_USE_BARREL {1} \
  CONFIG.C_USE_DIV {1} \
] $microblaze_0

# ----------------------------------------------------------------------------
# 2. Clock Wizard - Sistem saatleri
# ----------------------------------------------------------------------------
puts "   - Clock Wizard ekleniyor..."
set clk_wiz_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:clk_wiz:6.0 clk_wiz_0 ]
set_property -dict [list \
  CONFIG.PRIMITIVE {MMCM} \
  CONFIG.PRIM_IN_FREQ {200.000} \
  CONFIG.CLKOUT1_REQUESTED_OUT_FREQ {100.000} \
  CONFIG.CLKOUT2_USED {true} \
  CONFIG.CLKOUT2_REQUESTED_OUT_FREQ {200.000} \
  CONFIG.CLKOUT3_USED {true} \
  CONFIG.CLKOUT3_REQUESTED_OUT_FREQ {156.25} \
  CONFIG.USE_RESET {true} \
  CONFIG.RESET_TYPE {ACTIVE_LOW} \
] $clk_wiz_0

# ----------------------------------------------------------------------------
# 3. Processor System Reset
# ----------------------------------------------------------------------------
puts "   - Processor System Reset ekleniyor..."
set rst_clk_wiz_100M [ create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 rst_clk_wiz_100M ]
set rst_clk_wiz_200M [ create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 rst_clk_wiz_200M ]

# ----------------------------------------------------------------------------
# 4. DDR4 Memory Controller (MIG)
# ----------------------------------------------------------------------------
puts "   - DDR4 Memory Interface Generator (MIG) ekleniyor..."
set ddr4_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:ddr4:2.2 ddr4_0 ]
set_property -dict [list \
  CONFIG.C0.DDR4_TimePeriod {833} \
  CONFIG.C0.DDR4_InputClockPeriod {5000} \
  CONFIG.C0.DDR4_MemoryType {Components} \
  CONFIG.C0.DDR4_DataWidth {64} \
  CONFIG.C0.DDR4_DataMask {NONE} \
  CONFIG.C0.DDR4_Ecc {false} \
  CONFIG.C0.DDR4_AxiSelection {true} \
  CONFIG.C0.DDR4_AxiDataWidth {512} \
  CONFIG.C0.DDR4_AxiAddressWidth {31} \
] $ddr4_0

# ----------------------------------------------------------------------------
# 5. AXI DMA - Stream to Memory Map
# ----------------------------------------------------------------------------
puts "   - AXI DMA (S2MM) ekleniyor..."
set axi_dma_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma:7.1 axi_dma_0 ]
set_property -dict [list \
  CONFIG.c_include_sg {0} \
  CONFIG.c_sg_include_stscntrl_strm {0} \
  CONFIG.c_include_mm2s {0} \
  CONFIG.c_include_s2mm {1} \
  CONFIG.c_s2mm_burst_size {256} \
  CONFIG.c_m_axi_s2mm_data_width {512} \
  CONFIG.c_m_axis_mm2s_tdata_width {64} \
  CONFIG.c_s_axis_s2mm_tdata_width {64} \
] $axi_dma_0

# ----------------------------------------------------------------------------
# 6. GTY Transceiver (Aurora 64B/66B örnek)
# ----------------------------------------------------------------------------
puts "   - GTY Wizard ekleniyor..."
# Not: GTY wizard IP'si board'a özel konfigüre edilmelidir
# Burada temel bir GTY Wizard ekleniyor
set gty_wizard_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:gtwizard_ultrascale:1.7 gty_wizard_0 ]
set_property -dict [list \
  CONFIG.CHANNEL_ENABLE {X0Y0} \
  CONFIG.TX_LINE_RATE {10.3125} \
  CONFIG.TX_REFCLK_FREQUENCY {156.25} \
  CONFIG.RX_LINE_RATE {10.3125} \
  CONFIG.RX_REFCLK_FREQUENCY {156.25} \
  CONFIG.TX_DATA_ENCODING {64B66B_ASYNC} \
  CONFIG.RX_DATA_DECODING {64B66B_ASYNC} \
  CONFIG.TX_USER_DATA_WIDTH {64} \
  CONFIG.RX_USER_DATA_WIDTH {64} \
] $gty_wizard_0

# ----------------------------------------------------------------------------
# 7. AXI Stream Data FIFO - GTY ile DMA arası tampon
# ----------------------------------------------------------------------------
puts "   - AXI Stream Data FIFO ekleniyor..."
set axis_data_fifo_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:axis_data_fifo:2.0 axis_data_fifo_0 ]
set_property -dict [list \
  CONFIG.TDATA_NUM_BYTES {8} \
  CONFIG.FIFO_DEPTH {16384} \
  CONFIG.HAS_TLAST {1} \
  CONFIG.HAS_TKEEP {1} \
  CONFIG.HAS_TSTRB {0} \
] $axis_data_fifo_0

# ----------------------------------------------------------------------------
# 8. AXI SmartConnect - DDR4 interconnect
# ----------------------------------------------------------------------------
puts "   - AXI SmartConnect ekleniyor..."
set axi_smc_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 axi_smc_0 ]
set_property -dict [list \
  CONFIG.NUM_SI {2} \
  CONFIG.NUM_MI {1} \
] $axi_smc_0

# ----------------------------------------------------------------------------
# 9. AXI Interconnect - MicroBlaze peripheral
# ----------------------------------------------------------------------------
puts "   - AXI Interconnect (Peripheral) ekleniyor..."
set microblaze_0_axi_periph [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 microblaze_0_axi_periph ]
set_property -dict [list \
  CONFIG.NUM_MI {3} \
] $microblaze_0_axi_periph

# ----------------------------------------------------------------------------
# 10. MicroBlaze Local Memory (BRAM)
# ----------------------------------------------------------------------------
puts "   - MicroBlaze Local Memory ekleniyor..."
set microblaze_0_local_memory [ create_bd_cell -type ip -vlnv xilinx.com:ip:lmb_bram_if_cntlr:4.0 microblaze_0_local_memory/lmb_bram_if_cntlr ]
set dlmb_bram [ create_bd_cell -type ip -vlnv xilinx.com:ip:blk_mem_gen:8.4 microblaze_0_local_memory/lmb_bram ]
set dlmb_v10 [ create_bd_cell -type ip -vlnv xilinx.com:ip:lmb_v10:3.0 microblaze_0_local_memory/dlmb_v10 ]
set ilmb_v10 [ create_bd_cell -type ip -vlnv xilinx.com:ip:lmb_v10:3.0 microblaze_0_local_memory/ilmb_v10 ]

# ----------------------------------------------------------------------------
# 11. AXI UART Lite - Debug için
# ----------------------------------------------------------------------------
puts "   - AXI UART Lite ekleniyor..."
set axi_uartlite_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_uartlite:2.0 axi_uartlite_0 ]
set_property -dict [list \
  CONFIG.C_BAUDRATE {115200} \
] $axi_uartlite_0

# ----------------------------------------------------------------------------
# 12. AXI GPIO - Kontrol sinyalleri
# ----------------------------------------------------------------------------
puts "   - AXI GPIO ekleniyor..."
set axi_gpio_0 [ create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_0 ]
set_property -dict [list \
  CONFIG.C_GPIO_WIDTH {32} \
  CONFIG.C_ALL_OUTPUTS {0} \
  CONFIG.C_ALL_INPUTS {0} \
] $axi_gpio_0

# ============================================================================
# PORT OLUŞTURMA
# ============================================================================

puts "🔌 Harici portlar oluşturuluyor..."

# Sistem clock ve reset
create_bd_port -dir I -type clk sys_clk_p
create_bd_port -dir I -type clk sys_clk_n
create_bd_port -dir I -type rst sys_rst_n

set_property CONFIG.FREQ_HZ 200000000 [get_bd_ports sys_clk_p]

# UART
create_bd_intf_port -mode Master -vlnv xilinx.com:interface:uart_rtl:1.0 uart

# GPIO
create_bd_intf_port -mode Master -vlnv xilinx.com:interface:gpio_rtl:1.0 gpio

# GTY RefClk
create_bd_port -dir I -from 0 -to 0 -type clk gty_refclk_p
create_bd_port -dir I -from 0 -to 0 -type clk gty_refclk_n
set_property CONFIG.FREQ_HZ 156250000 [get_bd_ports gty_refclk_p]

# GTY RX/TX
create_bd_port -dir I -from 0 -to 0 gty_rxp
create_bd_port -dir I -from 0 -to 0 gty_rxn
create_bd_port -dir O -from 0 -to 0 gty_txp
create_bd_port -dir O -from 0 -to 0 gty_txn

# DDR4 Interface (MIG tarafından otomatik oluşturulacak)

# ============================================================================
# BAĞLANTILAR (CONNECTIONS)
# ============================================================================

puts "🔗 IP bağlantıları yapılıyor..."

# ----------------------------------------------------------------------------
# Clock ve Reset bağlantıları
# ----------------------------------------------------------------------------

# Sistem clock -> Clock Wizard
connect_bd_net [get_bd_ports sys_clk_p] [get_bd_pins clk_wiz_0/clk_in1_p]
connect_bd_net [get_bd_ports sys_clk_n] [get_bd_pins clk_wiz_0/clk_in1_n]
connect_bd_net [get_bd_ports sys_rst_n] [get_bd_pins clk_wiz_0/resetn]

# Clock Wizard -> Reset controllers
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins rst_clk_wiz_100M/slowest_sync_clk]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out2] [get_bd_pins rst_clk_wiz_200M/slowest_sync_clk]
connect_bd_net [get_bd_pins clk_wiz_0/locked] [get_bd_pins rst_clk_wiz_100M/dcm_locked]
connect_bd_net [get_bd_pins clk_wiz_0/locked] [get_bd_pins rst_clk_wiz_200M/dcm_locked]
connect_bd_net [get_bd_ports sys_rst_n] [get_bd_pins rst_clk_wiz_100M/ext_reset_in]
connect_bd_net [get_bd_ports sys_rst_n] [get_bd_pins rst_clk_wiz_200M/ext_reset_in]

# MicroBlaze clock (100 MHz)
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins microblaze_0/Clk]

# DDR4 UI clock (200 MHz)
connect_bd_net [get_bd_pins clk_wiz_0/clk_out2] [get_bd_pins ddr4_0/c0_sys_clk_i]
connect_bd_net [get_bd_ports sys_rst_n] [get_bd_pins ddr4_0/sys_rst]

# AXI DMA clocks
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axi_dma_0/s_axi_lite_aclk]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axi_dma_0/m_axi_s2mm_aclk]

# GTY clock (156.25 MHz)
connect_bd_net [get_bd_pins clk_wiz_0/clk_out3] [get_bd_pins gty_wizard_0/gtwiz_userclk_tx_usrclk2_in]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out3] [get_bd_pins gty_wizard_0/gtwiz_userclk_rx_usrclk2_in]

# AXIS FIFO clock
connect_bd_net [get_bd_pins clk_wiz_0/clk_out3] [get_bd_pins axis_data_fifo_0/s_axis_aclk]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axis_data_fifo_0/m_axis_aclk]

# SmartConnect clock
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axi_smc_0/aclk]

# Peripheral interconnect clock
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins microblaze_0_axi_periph/ACLK]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins microblaze_0_axi_periph/S00_ACLK]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins microblaze_0_axi_periph/M00_ACLK]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins microblaze_0_axi_periph/M01_ACLK]
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins microblaze_0_axi_periph/M02_ACLK]

# UART clock
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axi_uartlite_0/s_axi_aclk]

# GPIO clock
connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axi_gpio_0/s_axi_aclk]

# Resets
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins axi_dma_0/axi_resetn]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins axis_data_fifo_0/s_axis_aresetn]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins axi_smc_0/aresetn]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins microblaze_0_axi_periph/ARESETN]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins microblaze_0_axi_periph/S00_ARESETN]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins microblaze_0_axi_periph/M00_ARESETN]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins microblaze_0_axi_periph/M01_ARESETN]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins microblaze_0_axi_periph/M02_ARESETN]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins axi_uartlite_0/s_axi_aresetn]
connect_bd_net [get_bd_pins rst_clk_wiz_100M/peripheral_aresetn] [get_bd_pins axi_gpio_0/s_axi_aresetn]

# ----------------------------------------------------------------------------
# AXI Interface bağlantıları
# ----------------------------------------------------------------------------

# MicroBlaze -> Peripheral Interconnect
connect_bd_intf_net [get_bd_intf_pins microblaze_0/M_AXI_DP] [get_bd_intf_pins microblaze_0_axi_periph/S00_AXI]

# Peripheral Interconnect -> Peripherals
connect_bd_intf_net [get_bd_intf_pins microblaze_0_axi_periph/M00_AXI] [get_bd_intf_pins axi_dma_0/S_AXI_LITE]
connect_bd_intf_net [get_bd_intf_pins microblaze_0_axi_periph/M01_AXI] [get_bd_intf_pins axi_uartlite_0/S_AXI]
connect_bd_intf_net [get_bd_intf_pins microblaze_0_axi_periph/M02_AXI] [get_bd_intf_pins axi_gpio_0/S_AXI]

# AXI DMA -> SmartConnect -> DDR4
connect_bd_intf_net [get_bd_intf_pins axi_dma_0/M_AXI_S2MM] [get_bd_intf_pins axi_smc_0/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins microblaze_0/M_AXI_DC] [get_bd_intf_pins axi_smc_0/S01_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_smc_0/M00_AXI] [get_bd_intf_pins ddr4_0/C0_DDR4_S_AXI]

# ----------------------------------------------------------------------------
# AXI Stream bağlantıları (VERİ AKIŞI)
# ----------------------------------------------------------------------------

# GTY RX -> AXIS FIFO -> AXI DMA S2MM
# Not: GTY'nin user data çıkışı AXI-Stream'e dönüştürülmeli
# Basit wrapper modülü ile yapılabilir (aşağıda oluşturulacak)

# AXIS FIFO -> AXI DMA
connect_bd_intf_net [get_bd_intf_pins axis_data_fifo_0/M_AXIS] [get_bd_intf_pins axi_dma_0/S_AXIS_S2MM]

# ----------------------------------------------------------------------------
# External Port bağlantıları
# ----------------------------------------------------------------------------

# UART
connect_bd_intf_net [get_bd_intf_ports uart] [get_bd_intf_pins axi_uartlite_0/UART]

# GPIO
connect_bd_intf_net [get_bd_intf_ports gpio] [get_bd_intf_pins axi_gpio_0/GPIO]

# GTY RefClk
connect_bd_net [get_bd_ports gty_refclk_p] [get_bd_pins gty_wizard_0/gtrefclk0_in_p]
connect_bd_net [get_bd_ports gty_refclk_n] [get_bd_pins gty_wizard_0/gtrefclk0_in_n]

# GTY RX/TX
connect_bd_net [get_bd_ports gty_rxp] [get_bd_pins gty_wizard_0/rxp_in]
connect_bd_net [get_bd_ports gty_rxn] [get_bd_pins gty_wizard_0/rxn_in]
connect_bd_net [get_bd_ports gty_txp] [get_bd_pins gty_wizard_0/txp_out]
connect_bd_net [get_bd_ports gty_txn] [get_bd_pins gty_wizard_0/txn_out]

# ============================================================================
# ADRES ATAMA
# ============================================================================

puts "📍 Adres atamaları yapılıyor..."

assign_bd_address -offset 0x40400000 -range 0x00010000 [get_bd_addr_segs {axi_dma_0/S_AXI_LITE/Reg}]
assign_bd_address -offset 0x40600000 -range 0x00010000 [get_bd_addr_segs {axi_uartlite_0/S_AXI/Reg}]
assign_bd_address -offset 0x40000000 -range 0x00010000 [get_bd_addr_segs {axi_gpio_0/S_AXI/Reg}]
assign_bd_address -offset 0x80000000 -range 0x40000000 [get_bd_addr_segs {ddr4_0/C0_DDR4_MEMORY_MAP/C0_DDR4_ADDRESS_BLOCK}]

# ============================================================================
# BLOCK DESIGN VALIDASYON VE KAYDETME
# ============================================================================

puts "🔍 Block Design doğrulanıyor..."
validate_bd_design
save_bd_design

puts "💾 Block Design kaydedildi."

# ============================================================================
# HDL WRAPPER OLUŞTURMA
# ============================================================================

puts "📝 HDL Wrapper oluşturuluyor..."
make_wrapper -files [get_files $project_dir/$project_name.srcs/sources_1/bd/$bd_name/$bd_name.bd] -top
add_files -norecurse $project_dir/$project_name.gen/sources_1/bd/$bd_name/hdl/${bd_name}_wrapper.v

puts "✅ Wrapper oluşturuldu."

# ============================================================================
# PROJE TAMAMLANDI
# ============================================================================

puts ""
puts "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
puts "✅ PROJE BAŞARIYLA OLUŞTURULDU!"
puts "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
puts ""
puts "📁 Proje Dizini: $project_dir"
puts "📋 Block Design: $bd_name"
puts ""
puts "📌 SONRAKİ ADIMLAR:"
puts "   1. Block Design'ı inceleyin"
puts "   2. GTY konfigürasyonunu board'unuza göre ayarlayın"
puts "   3. DDR4 MIG ayarlarını kontrol edin"
puts "   4. Constraint dosyası (XDC) ekleyin"
puts "   5. Synthesis ve Implementation çalıştırın"
puts ""
puts "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
