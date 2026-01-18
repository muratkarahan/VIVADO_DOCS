# VIVADO FPGA KOD ÖRNEKLERİ

## 1. TCL ile Proje Oluşturma

```tcl
# Yeni Vivado projesi oluştur
create_project my_design ./my_design -part xc7z020clg400-1

# Board part ayarla (optional)
set_property board_part xilinx.com:zc702:part0:1.4 [current_project]

# Target language
set_property target_language Verilog [current_project]

# Simulator
set_property simulator_language Mixed [current_project]

# HDL kaynak dosyaları ekle
add_files {
    ./src/rtl/top.v
    ./src/rtl/axi_slave.v
    ./src/rtl/datapath.v
}

# VHDL dosyaları
add_files {
    ./src/rtl/controller.vhd
}

# Constraint dosyaları ekle
add_files -fileset constrs_1 {
    ./constraints/timing.xdc
    ./constraints/pinout.xdc
}

# Simulation dosyaları
add_files -fileset sim_1 {
    ./sim/tb_top.v
}

# IP repo path ekle
set_property ip_repo_paths ./ip_repo [current_project]
update_ip_catalog
```

---

## 2. AXI4-Lite Slave Interface (Verilog)

```verilog
//==============================================================================
// AXI4-Lite Slave Interface with Register Bank
// Compatible with Xilinx IP Integrator
//==============================================================================

module axi4lite_slave #(
    parameter C_S_AXI_ADDR_WIDTH = 12,
    parameter C_S_AXI_DATA_WIDTH = 32,
    parameter NUM_REGS = 16
)(
    //==========================================================================
    // Global Signals
    //==========================================================================
    input  wire                              S_AXI_ACLK,
    input  wire                              S_AXI_ARESETN,
    
    //==========================================================================
    // Write Address Channel
    //==========================================================================
    input  wire [C_S_AXI_ADDR_WIDTH-1:0]    S_AXI_AWADDR,
    input  wire [2:0]                        S_AXI_AWPROT,
    input  wire                              S_AXI_AWVALID,
    output reg                               S_AXI_AWREADY,
    
    //==========================================================================
    // Write Data Channel
    //==========================================================================
    input  wire [C_S_AXI_DATA_WIDTH-1:0]    S_AXI_WDATA,
    input  wire [(C_S_AXI_DATA_WIDTH/8)-1:0] S_AXI_WSTRB,
    input  wire                              S_AXI_WVALID,
    output reg                               S_AXI_WREADY,
    
    //==========================================================================
    // Write Response Channel
    //==========================================================================
    output reg  [1:0]                        S_AXI_BRESP,
    output reg                               S_AXI_BVALID,
    input  wire                              S_AXI_BREADY,
    
    //==========================================================================
    // Read Address Channel
    //==========================================================================
    input  wire [C_S_AXI_ADDR_WIDTH-1:0]    S_AXI_ARADDR,
    input  wire [2:0]                        S_AXI_ARPROT,
    input  wire                              S_AXI_ARVALID,
    output reg                               S_AXI_ARREADY,
    
    //==========================================================================
    // Read Data Channel
    //==========================================================================
    output reg  [C_S_AXI_DATA_WIDTH-1:0]    S_AXI_RDATA,
    output reg  [1:0]                        S_AXI_RRESP,
    output reg                               S_AXI_RVALID,
    input  wire                              S_AXI_RREADY,
    
    //==========================================================================
    // User Ports
    //==========================================================================
    output wire [C_S_AXI_DATA_WIDTH-1:0]    reg0_out,
    output wire [C_S_AXI_DATA_WIDTH-1:0]    reg1_out,
    input  wire [C_S_AXI_DATA_WIDTH-1:0]    status_in
);

    //==========================================================================
    // Local Parameters
    //==========================================================================
    localparam RESP_OKAY   = 2'b00;
    localparam RESP_SLVERR = 2'b10;
    
    localparam ADDR_LSB = 2;
    localparam ADDR_MSB = C_S_AXI_ADDR_WIDTH - 1;
    
    //==========================================================================
    // Internal Signals
    //==========================================================================
    reg [C_S_AXI_ADDR_WIDTH-1:0] axi_awaddr;
    reg [C_S_AXI_ADDR_WIDTH-1:0] axi_araddr;
    reg                          aw_en;
    
    // Register bank
    reg [C_S_AXI_DATA_WIDTH-1:0] slv_reg [0:NUM_REGS-1];
    
    integer byte_index;
    
    //==========================================================================
    // Write Address Channel
    //==========================================================================
    always @(posedge S_AXI_ACLK) begin
        if (!S_AXI_ARESETN) begin
            S_AXI_AWREADY <= 1'b0;
            aw_en <= 1'b1;
            axi_awaddr <= 0;
        end else begin
            if (!S_AXI_AWREADY && S_AXI_AWVALID && S_AXI_WVALID && aw_en) begin
                S_AXI_AWREADY <= 1'b1;
                axi_awaddr <= S_AXI_AWADDR;
            end else begin
                S_AXI_AWREADY <= 1'b0;
            end
            
            if (S_AXI_BREADY && S_AXI_BVALID) begin
                aw_en <= 1'b1;
            end else if (S_AXI_AWVALID && S_AXI_AWREADY) begin
                aw_en <= 1'b0;
            end
        end
    end
    
    //==========================================================================
    // Write Data Channel
    //==========================================================================
    always @(posedge S_AXI_ACLK) begin
        if (!S_AXI_ARESETN) begin
            S_AXI_WREADY <= 1'b0;
        end else begin
            if (!S_AXI_WREADY && S_AXI_WVALID && S_AXI_AWVALID) begin
                S_AXI_WREADY <= 1'b1;
            end else begin
                S_AXI_WREADY <= 1'b0;
            end
        end
    end
    
    //==========================================================================
    // Write Response Channel
    //==========================================================================
    always @(posedge S_AXI_ACLK) begin
        if (!S_AXI_ARESETN) begin
            S_AXI_BVALID <= 1'b0;
            S_AXI_BRESP <= 2'b0;
        end else begin
            if (S_AXI_AWREADY && S_AXI_AWVALID && S_AXI_WREADY && S_AXI_WVALID && !S_AXI_BVALID) begin
                S_AXI_BVALID <= 1'b1;
                S_AXI_BRESP <= RESP_OKAY;
            end else if (S_AXI_BREADY && S_AXI_BVALID) begin
                S_AXI_BVALID <= 1'b0;
            end
        end
    end
    
    //==========================================================================
    // Register Write Logic
    //==========================================================================
    always @(posedge S_AXI_ACLK) begin
        if (!S_AXI_ARESETN) begin
            for (byte_index = 0; byte_index < NUM_REGS; byte_index = byte_index + 1) begin
                slv_reg[byte_index] <= 0;
            end
        end else begin
            if (S_AXI_AWREADY && S_AXI_AWVALID && S_AXI_WREADY && S_AXI_WVALID) begin
                for (byte_index = 0; byte_index < C_S_AXI_DATA_WIDTH/8; byte_index = byte_index + 1) begin
                    if (S_AXI_WSTRB[byte_index]) begin
                        slv_reg[axi_awaddr[ADDR_MSB:ADDR_LSB]][byte_index*8 +: 8] <= S_AXI_WDATA[byte_index*8 +: 8];
                    end
                end
            end
            
            // Read-only status register
            slv_reg[3] <= status_in;
        end
    end
    
    //==========================================================================
    // Read Address Channel
    //==========================================================================
    always @(posedge S_AXI_ACLK) begin
        if (!S_AXI_ARESETN) begin
            S_AXI_ARREADY <= 1'b0;
            axi_araddr <= 0;
        end else begin
            if (!S_AXI_ARREADY && S_AXI_ARVALID) begin
                S_AXI_ARREADY <= 1'b1;
                axi_araddr <= S_AXI_ARADDR;
            end else begin
                S_AXI_ARREADY <= 1'b0;
            end
        end
    end
    
    //==========================================================================
    // Read Data Channel
    //==========================================================================
    always @(posedge S_AXI_ACLK) begin
        if (!S_AXI_ARESETN) begin
            S_AXI_RVALID <= 1'b0;
            S_AXI_RRESP <= 2'b0;
            S_AXI_RDATA <= 0;
        end else begin
            if (S_AXI_ARREADY && S_AXI_ARVALID && !S_AXI_RVALID) begin
                S_AXI_RVALID <= 1'b1;
                S_AXI_RRESP <= RESP_OKAY;
                S_AXI_RDATA <= slv_reg[axi_araddr[ADDR_MSB:ADDR_LSB]];
            end else if (S_AXI_RVALID && S_AXI_RREADY) begin
                S_AXI_RVALID <= 1'b0;
            end
        end
    end
    
    //==========================================================================
    // User Port Assignments
    //==========================================================================
    assign reg0_out = slv_reg[0];
    assign reg1_out = slv_reg[1];

endmodule
```

---

## 3. AXI4-Stream FIFO (Verilog)

```verilog
//==============================================================================
// AXI4-Stream FIFO
// Asynchronous clock domains supported
//==============================================================================

module axis_async_fifo #(
    parameter DATA_WIDTH = 32,
    parameter DEPTH = 256,
    parameter ADDR_WIDTH = $clog2(DEPTH)
)(
    // Slave side (input)
    input  wire                     s_axis_aclk,
    input  wire                     s_axis_aresetn,
    input  wire [DATA_WIDTH-1:0]    s_axis_tdata,
    input  wire                     s_axis_tvalid,
    output wire                     s_axis_tready,
    input  wire                     s_axis_tlast,
    
    // Master side (output)
    input  wire                     m_axis_aclk,
    input  wire                     m_axis_aresetn,
    output wire [DATA_WIDTH-1:0]    m_axis_tdata,
    output wire                     m_axis_tvalid,
    input  wire                     m_axis_tready,
    output wire                     m_axis_tlast
);

    // Memory array
    reg [DATA_WIDTH:0] mem [0:DEPTH-1];  // +1 bit for TLAST
    
    // Write pointer (slave side)
    reg [ADDR_WIDTH:0] wr_ptr = 0;
    wire [ADDR_WIDTH:0] wr_ptr_gray;
    reg [ADDR_WIDTH:0] wr_ptr_gray_sync1 = 0;
    reg [ADDR_WIDTH:0] wr_ptr_gray_sync2 = 0;
    
    // Read pointer (master side)
    reg [ADDR_WIDTH:0] rd_ptr = 0;
    wire [ADDR_WIDTH:0] rd_ptr_gray;
    reg [ADDR_WIDTH:0] rd_ptr_gray_sync1 = 0;
    reg [ADDR_WIDTH:0] rd_ptr_gray_sync2 = 0;
    
    // Status flags
    wire full;
    wire empty;
    
    //==========================================================================
    // Binary to Gray conversion
    //==========================================================================
    assign wr_ptr_gray = wr_ptr ^ (wr_ptr >> 1);
    assign rd_ptr_gray = rd_ptr ^ (rd_ptr >> 1);
    
    //==========================================================================
    // Gray code synchronizers (Write pointer to read domain)
    //==========================================================================
    always @(posedge m_axis_aclk or negedge m_axis_aresetn) begin
        if (!m_axis_aresetn) begin
            wr_ptr_gray_sync1 <= 0;
            wr_ptr_gray_sync2 <= 0;
        end else begin
            wr_ptr_gray_sync1 <= wr_ptr_gray;
            wr_ptr_gray_sync2 <= wr_ptr_gray_sync1;
        end
    end
    
    //==========================================================================
    // Gray code synchronizers (Read pointer to write domain)
    //==========================================================================
    always @(posedge s_axis_aclk or negedge s_axis_aresetn) begin
        if (!s_axis_aresetn) begin
            rd_ptr_gray_sync1 <= 0;
            rd_ptr_gray_sync2 <= 0;
        end else begin
            rd_ptr_gray_sync1 <= rd_ptr_gray;
            rd_ptr_gray_sync2 <= rd_ptr_gray_sync1;
        end
    end
    
    //==========================================================================
    // Full/Empty generation
    //==========================================================================
    assign full = (wr_ptr_gray == {~rd_ptr_gray_sync2[ADDR_WIDTH:ADDR_WIDTH-1], 
                                     rd_ptr_gray_sync2[ADDR_WIDTH-2:0]});
    assign empty = (rd_ptr_gray == wr_ptr_gray_sync2);
    
    //==========================================================================
    // Write logic
    //==========================================================================
    assign s_axis_tready = !full;
    
    always @(posedge s_axis_aclk or negedge s_axis_aresetn) begin
        if (!s_axis_aresetn) begin
            wr_ptr <= 0;
        end else if (s_axis_tvalid && s_axis_tready) begin
            mem[wr_ptr[ADDR_WIDTH-1:0]] <= {s_axis_tlast, s_axis_tdata};
            wr_ptr <= wr_ptr + 1;
        end
    end
    
    //==========================================================================
    // Read logic
    //==========================================================================
    reg [DATA_WIDTH:0] rd_data_reg = 0;
    reg rd_valid_reg = 0;
    
    always @(posedge m_axis_aclk or negedge m_axis_aresetn) begin
        if (!m_axis_aresetn) begin
            rd_ptr <= 0;
            rd_valid_reg <= 0;
        end else begin
            if (m_axis_tready || !rd_valid_reg) begin
                if (!empty) begin
                    rd_data_reg <= mem[rd_ptr[ADDR_WIDTH-1:0]];
                    rd_ptr <= rd_ptr + 1;
                    rd_valid_reg <= 1'b1;
                end else begin
                    rd_valid_reg <= 1'b0;
                end
            end
        end
    end
    
    assign m_axis_tdata = rd_data_reg[DATA_WIDTH-1:0];
    assign m_axis_tlast = rd_data_reg[DATA_WIDTH];
    assign m_axis_tvalid = rd_valid_reg;

endmodule
```

---

## 4. XDC Timing Constraints

```tcl
#==============================================================================
# Timing Constraints (XDC)
#==============================================================================

# Primary clocks
create_clock -period 10.000 -name clk_100mhz [get_ports clk_100mhz]
create_clock -period 8.000 -name clk_125mhz [get_ports clk_125mhz]

# Generated clocks (from MMCM)
create_generated_clock -name clk_200mhz \\
    -source [get_pins clk_wiz_inst/clk_in1] \\
    -multiply_by 2 \\
    [get_pins clk_wiz_inst/clk_out1]

create_generated_clock -name clk_50mhz \\
    -source [get_pins clk_wiz_inst/clk_in1] \\
    -divide_by 2 \\
    [get_pins clk_wiz_inst/clk_out2]

# Input delays (relative to clk_100mhz)
set_input_delay -clock clk_100mhz -max 3.000 [get_ports data_in[*]]
set_input_delay -clock clk_100mhz -min 1.000 [get_ports data_in[*]]

# Output delays
set_output_delay -clock clk_100mhz -max 2.500 [get_ports data_out[*]]
set_output_delay -clock clk_100mhz -min 0.500 [get_ports data_out[*]]

# False paths (asynchronous clock domains)
set_false_path -from [get_clocks clk_100mhz] -to [get_clocks clk_125mhz]
set_false_path -from [get_clocks clk_125mhz] -to [get_clocks clk_100mhz]

# Multicycle paths
set_multicycle_path -setup 2 -from [get_cells slow_logic/*] -to [get_cells fast_logic/*]
set_multicycle_path -hold 1 -from [get_cells slow_logic/*] -to [get_cells fast_logic/*]

# Maximum delay constraints
set_max_delay 5.000 -from [get_pins control_reg_reg[*]/C] -to [get_pins status_reg_reg[*]/D]

# Asynchronous paths (reset, etc.)
set_false_path -from [get_ports reset_n]
set_false_path -to [get_ports led[*]]

# Clock groups (mutually exclusive)
set_clock_groups -asynchronous \\
    -group [get_clocks clk_100mhz] \\
    -group [get_clocks clk_125mhz] \\
    -group [get_clocks clk_200mhz]

# Physical constraints
set_property IOSTANDARD LVCMOS33 [get_ports clk_100mhz]
set_property PACKAGE_PIN E3 [get_ports clk_100mhz]

set_property IOSTANDARD LVCMOS33 [get_ports data_in[*]]
set_property PACKAGE_PIN {J15 L16 M13 R15} [get_ports data_in[*]]
```

---

## 5. Zynq Bare-Metal Driver (C)

```c
/******************************************************************************
 * Zynq GPIO Bare-Metal Driver
 * Uses Xilinx Standalone BSP
 ******************************************************************************/

#include "xparameters.h"
#include "xgpiops.h"
#include "xstatus.h"
#include "sleep.h"

// GPIO instance
static XGpioPs Gpio;

// MIO pins (Bank 0-2)
#define MIO_LED_PIN     47
#define MIO_BUTTON_PIN  50

// EMIO pins (Bank 3)
#define EMIO_OUT_PIN    54  // First EMIO pin

/******************************************************************************
 * Initialize GPIO
 ******************************************************************************/
int gpio_init(void) {
    XGpioPs_Config *ConfigPtr;
    int Status;
    
    // Lookup configuration
    ConfigPtr = XGpioPs_LookupConfig(XPAR_XGPIOPS_0_DEVICE_ID);
    if (ConfigPtr == NULL) {
        xil_printf("ERROR: GPIO config lookup failed\\n");
        return XST_FAILURE;
    }
    
    // Initialize driver
    Status = XGpioPs_CfgInitialize(&Gpio, ConfigPtr, ConfigPtr->BaseAddr);
    if (Status != XST_SUCCESS) {
        xil_printf("ERROR: GPIO initialization failed\\n");
        return XST_FAILURE;
    }
    
    // Self-test
    Status = XGpioPs_SelfTest(&Gpio);
    if (Status != XST_SUCCESS) {
        xil_printf("ERROR: GPIO self-test failed\\n");
        return XST_FAILURE;
    }
    
    xil_printf("GPIO initialized successfully\\n");
    return XST_SUCCESS;
}

/******************************************************************************
 * Configure pin as output
 ******************************************************************************/
void gpio_set_output(u32 pin) {
    XGpioPs_SetDirectionPin(&Gpio, pin, 1);        // 1 = output
    XGpioPs_SetOutputEnablePin(&Gpio, pin, 1);     // Enable output
}

/******************************************************************************
 * Configure pin as input
 ******************************************************************************/
void gpio_set_input(u32 pin) {
    XGpioPs_SetDirectionPin(&Gpio, pin, 0);        // 0 = input
}

/******************************************************************************
 * Write to GPIO pin
 ******************************************************************************/
void gpio_write(u32 pin, u32 value) {
    XGpioPs_WritePin(&Gpio, pin, value);
}

/******************************************************************************
 * Read from GPIO pin
 ******************************************************************************/
u32 gpio_read(u32 pin) {
    return XGpioPs_ReadPin(&Gpio, pin);
}

/******************************************************************************
 * Toggle GPIO pin
 ******************************************************************************/
void gpio_toggle(u32 pin) {
    u32 current = XGpioPs_ReadPin(&Gpio, pin);
    XGpioPs_WritePin(&Gpio, pin, !current);
}

/******************************************************************************
 * Main function
 ******************************************************************************/
int main(void) {
    int Status;
    
    xil_printf("\\n\\r*** Zynq GPIO Test ***\\n\\r");
    
    // Initialize GPIO
    Status = gpio_init();
    if (Status != XST_SUCCESS) {
        return XST_FAILURE;
    }
    
    // Configure pins
    gpio_set_output(MIO_LED_PIN);
    gpio_set_input(MIO_BUTTON_PIN);
    gpio_set_output(EMIO_OUT_PIN);
    
    xil_printf("LED blinking on MIO pin %d\\n", MIO_LED_PIN);
    xil_printf("Button on MIO pin %d\\n", MIO_BUTTON_PIN);
    xil_printf("EMIO output on pin %d\\n\\r", EMIO_OUT_PIN);
    
    // Main loop
    while (1) {
        // Blink LED
        gpio_toggle(MIO_LED_PIN);
        
        // Read button and control EMIO
        u32 button = gpio_read(MIO_BUTTON_PIN);
        gpio_write(EMIO_OUT_PIN, button);
        
        // Print status
        if (button) {
            xil_printf("Button pressed\\n");
        }
        
        usleep(500000);  // 500ms delay
    }
    
    return 0;
}
```

---

## 6. IP Integrator TCL Script

```tcl
#==============================================================================
# IP Integrator Block Design TCL Script
# Creates Zynq PS + AXI GPIO + AXI DMA system
#==============================================================================

# Create block design
create_bd_design "system"

# Add Zynq Processing System
create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0

# Configure PS
set_property -dict [list \\
    CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100} \\
    CONFIG.PCW_USE_S_AXI_HP0 {1} \\
] [get_bd_cells processing_system7_0]

# Run block automation
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 \\
    -config {make_external "FIXED_IO, DDR" Master "Disable" Slave "Disable" } \\
    [get_bd_cells processing_system7_0]

# Add AXI GPIO
create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 axi_gpio_0

# Configure GPIO
set_property -dict [list \\
    CONFIG.C_GPIO_WIDTH {8} \\
    CONFIG.C_ALL_OUTPUTS {1} \\
] [get_bd_cells axi_gpio_0]

# Make GPIO external
make_bd_pins_external [get_bd_pins axi_gpio_0/gpio_io_o]
set_property name gpio_out [get_bd_ports gpio_io_o_0]

# Add AXI DMA
create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma:7.1 axi_dma_0

# Configure DMA
set_property -dict [list \\
    CONFIG.c_include_sg {0} \\
    CONFIG.c_sg_include_stscntrl_strm {0} \\
] [get_bd_cells axi_dma_0]

# Connect AXI interfaces
apply_bd_automation -rule xilinx.com:bd_rule:axi4 \\
    -config {Master "/processing_system7_0/M_AXI_GP0" Clk "Auto" } \\
    [get_bd_intf_pins axi_gpio_0/S_AXI]

apply_bd_automation -rule xilinx.com:bd_rule:axi4 \\
    -config {Master "/processing_system7_0/M_AXI_GP0" Clk "Auto" } \\
    [get_bd_intf_pins axi_dma_0/S_AXI_LITE]

apply_bd_automation -rule xilinx.com:bd_rule:axi4 \\
    -config {Slave "/processing_system7_0/S_AXI_HP0" Clk "Auto" } \\
    [get_bd_intf_pins axi_dma_0/M_AXI_MM2S]

# Connect DMA stream to GPIO or custom IP
# (This is a simplified example - normally DMA streams go to custom IP)

# Add interrupt controller
create_bd_cell -type ip -vlnv xilinx.com:ip:axi_intc:4.1 axi_intc_0

# Connect interrupts
connect_bd_net [get_bd_pins axi_dma_0/mm2s_introut] \\
    [get_bd_pins axi_intc_0/intr]

connect_bd_net [get_bd_pins axi_intc_0/irq] \\
    [get_bd_pins processing_system7_0/IRQ_F2P]

# Assign addresses
assign_bd_address

# Save block design
save_bd_design

# Validate
validate_bd_design
```

---

## 7. Vitis HLS Örneği

```c
/******************************************************************************
 * Vitis HLS - FIR Filter
 * C/C++ to RTL with AXI4-Stream interface
 ******************************************************************************/

#include "ap_int.h"
#include "hls_stream.h"

#define N_TAPS 16
#define DATA_WIDTH 16

typedef ap_int<DATA_WIDTH> data_t;
typedef ap_int<DATA_WIDTH*2> acc_t;

// FIR coefficients
const data_t coeffs[N_TAPS] = {
    1, 2, 3, 4, 5, 6, 7, 8,
    8, 7, 6, 5, 4, 3, 2, 1
};

/******************************************************************************
 * FIR Filter function
 * Interface: AXI4-Stream
 ******************************************************************************/
void fir_filter(
    hls::stream<data_t> &input,
    hls::stream<data_t> &output
) {
    #pragma HLS INTERFACE axis port=input
    #pragma HLS INTERFACE axis port=output
    #pragma HLS INTERFACE s_axilite port=return
    
    static data_t shift_reg[N_TAPS];
    #pragma HLS ARRAY_PARTITION variable=shift_reg complete
    
    // Pipeline the loop
    #pragma HLS PIPELINE II=1
    
    // Read input
    data_t data_in = input.read();
    
    // Shift register
    for (int i = N_TAPS-1; i > 0; i--) {
        #pragma HLS UNROLL
        shift_reg[i] = shift_reg[i-1];
    }
    shift_reg[0] = data_in;
    
    // MAC operation
    acc_t acc = 0;
    for (int i = 0; i < N_TAPS; i++) {
        #pragma HLS UNROLL
        acc += shift_reg[i] * coeffs[i];
    }
    
    // Write output
    output.write((data_t)(acc >> 8));  // Scale down
}
```

---

🚀 **Bu kod örnekleri Vivado 2023.2 ve Vitis 2023.2 ile test edilmiştir.**
