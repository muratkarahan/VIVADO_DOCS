# ============================================================================
# Virtex-7 GTY to DDR4 via AXI DMA - Constraint Dosyası (XDC)
# ============================================================================
# Bu dosya pin atamaları, timing constraint'leri ve fiziksel yerleşim
# kısıtlamalarını içerir.
# ============================================================================
# NOT: Pin numaraları board'unuza göre değiştirilmelidir!
# ============================================================================

# ============================================================================
# SİSTEM CLOCK VE RESET
# ============================================================================

# Differential System Clock (200 MHz)
set_property PACKAGE_PIN E19 [get_ports sys_clk_p]
set_property PACKAGE_PIN E18 [get_ports sys_clk_n]
set_property IOSTANDARD DIFF_SSTL15 [get_ports sys_clk_p]
set_property IOSTANDARD DIFF_SSTL15 [get_ports sys_clk_n]

create_clock -period 5.000 -name sys_clk -waveform {0.000 2.500} [get_ports sys_clk_p]

# System Reset (Active Low)
set_property PACKAGE_PIN AV40 [get_ports sys_rst_n]
set_property IOSTANDARD LVCMOS18 [get_ports sys_rst_n]
set_property PULLUP true [get_ports sys_rst_n]

# ============================================================================
# GTY TRANSCEIVER PINS
# ============================================================================

# GTY Reference Clock (156.25 MHz)
# Bank 112 - MGTREFCLK0
set_property PACKAGE_PIN F6 [get_ports gty_refclk_p]
set_property PACKAGE_PIN F5 [get_ports gty_refclk_n]

create_clock -period 6.400 -name gty_refclk -waveform {0.000 3.200} [get_ports gty_refclk_p]

# GTY RX/TX Differential Pairs
# Bank 112 - Channel 0
set_property PACKAGE_PIN B8 [get_ports {gty_rxp[0]}]
set_property PACKAGE_PIN B7 [get_ports {gty_rxn[0]}]
set_property PACKAGE_PIN A6 [get_ports {gty_txp[0]}]
set_property PACKAGE_PIN A5 [get_ports {gty_txn[0]}]

# ============================================================================
# UART PINS
# ============================================================================

set_property PACKAGE_PIN AU36 [get_ports uart_rxd]
set_property PACKAGE_PIN AU33 [get_ports uart_txd]
set_property IOSTANDARD LVCMOS18 [get_ports uart_rxd]
set_property IOSTANDARD LVCMOS18 [get_ports uart_txd]

# ============================================================================
# GPIO - LED PINS (Debug için)
# ============================================================================

set_property PACKAGE_PIN AM39 [get_ports {gpio_tri_o[0]}]
set_property PACKAGE_PIN AN39 [get_ports {gpio_tri_o[1]}]
set_property PACKAGE_PIN AR37 [get_ports {gpio_tri_o[2]}]
set_property PACKAGE_PIN AT37 [get_ports {gpio_tri_o[3]}]
set_property PACKAGE_PIN AR35 [get_ports {gpio_tri_o[4]}]
set_property PACKAGE_PIN AP41 [get_ports {gpio_tri_o[5]}]
set_property PACKAGE_PIN AP42 [get_ports {gpio_tri_o[6]}]
set_property PACKAGE_PIN AU39 [get_ports {gpio_tri_o[7]}]

set_property IOSTANDARD LVCMOS18 [get_ports {gpio_tri_o[*]}]

# ============================================================================
# DDR4 MEMORY INTERFACE
# ============================================================================
# NOT: DDR4 pin atamaları MIG IP tarafından otomatik oluşturulur.
# Eğer manuel pin assignment gerekiyorsa MIG'den export edilen
# XDC dosyası buraya dahil edilebilir.

# DDR4 Clock Groups - Asenkron
set_clock_groups -asynchronous \
    -group [get_clocks sys_clk] \
    -group [get_clocks -of_objects [get_pins ddr4_0/inst/u_ddr4_infrastructure/gen_mmcme*.u_mmcme_adv_inst/CLKOUT0]]

# ============================================================================
# GTY CLOCK GROUPS
# ============================================================================

# GTY recovered clock (asenkron)
set_clock_groups -asynchronous \
    -group [get_clocks gty_refclk] \
    -group [get_clocks sys_clk]

# GTY user clocks
set_clock_groups -asynchronous \
    -group [get_clocks -of_objects [get_pins gty_wizard_0/inst/gen_gtwizard_gtye4_top.gtwizard_ultrascale_v1_7_15_gtye4_common_wrapper_inst/rxoutclk_out]] \
    -group [get_clocks sys_clk]

# ============================================================================
# TIMİNG CONSTRAINTS
# ============================================================================

# AXI DMA veri yolu
set_max_delay -datapath_only -from [get_cells -hierarchical -filter {NAME =~ *axi_dma*}] 10.000
set_min_delay -from [get_cells -hierarchical -filter {NAME =~ *axi_dma*}] 2.000

# GTY to AXIS FIFO
set_max_delay -datapath_only -from [get_cells -hierarchical -filter {NAME =~ *gty_wizard*}] \
                               -to   [get_cells -hierarchical -filter {NAME =~ *axis_data_fifo*}] 8.000

# DDR4 Controller
set_multicycle_path -setup 2 -from [get_cells -hierarchical -filter {NAME =~ *ddr4_0*}]
set_multicycle_path -hold 1 -from [get_cells -hierarchical -filter {NAME =~ *ddr4_0*}]

# ============================================================================
# FALSE PATH - Asenkron Domain Geçişleri
# ============================================================================

# Reset sinyalleri
set_false_path -from [get_ports sys_rst_n]
set_false_path -to [get_pins -hierarchical -filter {NAME =~ *rst_clk_wiz*/peripheral_aresetn*}]

# GPIO static sinyalleri
set_false_path -to [get_ports {gpio_tri_o[*]}]

# ============================================================================
# FİZİKSEL YERLEŞIM KISITLAMALARI
# ============================================================================

# AXI DMA'yı DDR4 controller'a yakın yerleştir (performans için)
create_pblock pblock_dma_ddr4
resize_pblock pblock_dma_ddr4 -add {CLOCKREGION_X0Y0:CLOCKREGION_X1Y2}
add_cells_to_pblock pblock_dma_ddr4 [get_cells -hierarchical -filter {NAME =~ *axi_dma*}]
add_cells_to_pblock pblock_dma_ddr4 [get_cells -hierarchical -filter {NAME =~ *axi_smc*}]

# GTY ile AXIS FIFO aynı clock region'da olmalı
create_pblock pblock_gty_interface
resize_pblock pblock_gty_interface -add {CLOCKREGION_X0Y5:CLOCKREGION_X0Y6}
add_cells_to_pblock pblock_gty_interface [get_cells -hierarchical -filter {NAME =~ *axis_data_fifo*}]

# ============================================================================
# BITSTREAM AYARLARI
# ============================================================================

set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]
set_property CONFIG_VOLTAGE 1.8 [current_design]
set_property CFGBVS VCCO [current_design]
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property BITSTREAM.CONFIG.SPI_FALL_EDGE YES [current_design]

# ============================================================================
# DRC BYPASS (Gerekirse)
# ============================================================================

# GTY placement DRC bypass
set_property IS_LOC_FIXED false [get_cells -hierarchical -filter {NAME =~ *gty_wizard*}]

# ============================================================================
# REPORT AYARLARI
# ============================================================================

set_property SEVERITY {Warning} [get_drc_checks NSTD-1]
set_property SEVERITY {Warning} [get_drc_checks UCIO-1]

# ============================================================================
# CONSTRAINT DOSYASI SONU
# ============================================================================
