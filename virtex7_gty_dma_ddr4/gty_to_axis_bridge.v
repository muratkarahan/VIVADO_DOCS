// ============================================================================
// GTY RX Data to AXI-Stream Bridge Module
// ============================================================================
// Bu modül GTY transceiver'ın RX user data çıkışını AXI4-Stream formatına
// dönüştürür. AXI DMA ile uyumlu stream oluşturur.
// ============================================================================

`timescale 1ns / 1ps

module gty_to_axis_bridge #(
    parameter DATA_WIDTH = 64,  // GTY user data genişliği
    parameter PACKET_SIZE = 1024 // Paket boyutu (byte)
)(
    // Clock ve Reset
    input  wire                     aclk,
    input  wire                     aresetn,
    
    // GTY RX Interface
    input  wire [DATA_WIDTH-1:0]    gty_rx_data,
    input  wire                     gty_rx_valid,
    input  wire                     gty_rx_header_valid,
    input  wire [1:0]               gty_rx_header,
    output wire                     gty_rx_ready,
    
    // AXI4-Stream Master (to FIFO/DMA)
    output reg  [DATA_WIDTH-1:0]    m_axis_tdata,
    output reg                      m_axis_tvalid,
    output reg                      m_axis_tlast,
    output reg  [(DATA_WIDTH/8)-1:0] m_axis_tkeep,
    input  wire                     m_axis_tready
);

    // ========================================================================
    // İÇ SİNYALLER
    // ========================================================================
    
    reg [15:0] byte_counter;
    reg [15:0] packet_byte_count;
    
    wire transfer_active;
    wire packet_complete;
    
    assign transfer_active = m_axis_tvalid && m_axis_tready;
    assign packet_complete = (byte_counter >= packet_byte_count - (DATA_WIDTH/8));
    
    // ========================================================================
    // PAKET SAYACILARI
    // ========================================================================
    
    // Paket boyutu parametresi
    always @(posedge aclk) begin
        if (!aresetn) begin
            packet_byte_count <= PACKET_SIZE;
        end
    end
    
    // Byte sayacı - her transferde artar
    always @(posedge aclk) begin
        if (!aresetn) begin
            byte_counter <= 16'd0;
        end else if (transfer_active) begin
            if (m_axis_tlast) begin
                byte_counter <= 16'd0;
            end else begin
                byte_counter <= byte_counter + (DATA_WIDTH/8);
            end
        end
    end
    
    // ========================================================================
    // AXI-STREAM SINYAL OLUŞTURMA
    // ========================================================================
    
    // TDATA - Veriyi doğrudan aktar
    always @(posedge aclk) begin
        if (!aresetn) begin
            m_axis_tdata <= {DATA_WIDTH{1'b0}};
        end else if (gty_rx_valid && gty_rx_ready) begin
            m_axis_tdata <= gty_rx_data;
        end
    end
    
    // TVALID - GTY'den valid geldiğinde aktif
    always @(posedge aclk) begin
        if (!aresetn) begin
            m_axis_tvalid <= 1'b0;
        end else begin
            if (gty_rx_valid) begin
                m_axis_tvalid <= 1'b1;
            end else if (transfer_active) begin
                m_axis_tvalid <= 1'b0;
            end
        end
    end
    
    // TLAST - Paket sonunda aktif
    always @(posedge aclk) begin
        if (!aresetn) begin
            m_axis_tlast <= 1'b0;
        end else begin
            if (gty_rx_valid && packet_complete) begin
                m_axis_tlast <= 1'b1;
            end else if (transfer_active) begin
                m_axis_tlast <= 1'b0;
            end
        end
    end
    
    // TKEEP - Tüm byte'lar geçerli (hepsi 1)
    always @(posedge aclk) begin
        if (!aresetn) begin
            m_axis_tkeep <= {(DATA_WIDTH/8){1'b0}};
        end else begin
            m_axis_tkeep <= {(DATA_WIDTH/8){1'b1}};
        end
    end
    
    // GTY RX Ready - AXI-Stream tarafı hazırsa kabul et
    assign gty_rx_ready = m_axis_tready || !m_axis_tvalid;
    
    // ========================================================================
    // DEBUG VE PERFORMANS SAYAÇLARI (İsteğe Bağlı)
    // ========================================================================
    
    reg [31:0] total_packets;
    reg [31:0] total_bytes;
    
    always @(posedge aclk) begin
        if (!aresetn) begin
            total_packets <= 32'd0;
            total_bytes <= 32'd0;
        end else if (transfer_active) begin
            total_bytes <= total_bytes + (DATA_WIDTH/8);
            if (m_axis_tlast) begin
                total_packets <= total_packets + 1'b1;
            end
        end
    end

endmodule
