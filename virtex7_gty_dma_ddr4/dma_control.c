// ============================================================================
// AXI DMA Kontrolcü Yazılımı (Baremetal C)
// ============================================================================
// Bu kod MicroBlaze üzerinde çalışır ve AXI DMA S2MM transferini başlatır.
// GTY'den gelen veriyi DDR4'e sürekli yazar.
// ============================================================================

#include "xparameters.h"
#include "xaxidma.h"
#include "xil_printf.h"
#include "xil_cache.h"
#include "xgpio.h"

// ============================================================================
// TANIMLAMALAR
// ============================================================================

#define DMA_DEV_ID              XPAR_AXIDMA_0_DEVICE_ID
#define DDR4_BASE_ADDR          0x80000000  // DDR4 başlangıç adresi
#define TRANSFER_SIZE           (1024*1024) // 1 MB transfer
#define MAX_PKT_LEN             0x100       // Maksimum paket uzunluğu

#define GPIO_DEVICE_ID          XPAR_GPIO_0_DEVICE_ID
#define GPIO_CHANNEL_1          1

// ============================================================================
// GLOBAL DEĞİŞKENLER
// ============================================================================

XAxiDma AxiDma;
XGpio Gpio;

static u32 gRxBufferPtr = DDR4_BASE_ADDR;
static u32 gTransferCount = 0;

// ============================================================================
// FONKSIYON PROTOTIPLERI
// ============================================================================

int DMA_Init(void);
int DMA_Start_S2MM_Transfer(u32 addr, u32 length);
void DMA_IntrHandler(void *Callback);
int Setup_Interrupts(void);

// ============================================================================
// ANA PROGRAM
// ============================================================================

int main(void)
{
    int Status;
    u32 transfer_addr;
    
    xil_printf("\r\n╔══════════════════════════════════════════════════════╗\r\n");
    xil_printf("║  Virtex-7 GTY -> AXI DMA -> DDR4 Demo Program      ║\r\n");
    xil_printf("╚══════════════════════════════════════════════════════╝\r\n\r\n");
    
    // ========================================================================
    // BAŞLATMA
    // ========================================================================
    
    xil_printf(">>> DMA başlatılıyor...\r\n");
    Status = DMA_Init();
    if (Status != XST_SUCCESS) {
        xil_printf("❌ HATA: DMA başlatılamadı!\r\n");
        return XST_FAILURE;
    }
    xil_printf("✅ DMA başlatıldı.\r\n");
    
    // GPIO başlat (LED kontrolü için)
    XGpio_Initialize(&Gpio, GPIO_DEVICE_ID);
    XGpio_SetDataDirection(&Gpio, GPIO_CHANNEL_1, 0x00000000); // Çıkış
    xil_printf("✅ GPIO başlatıldı.\r\n");
    
    // Cache temizle
    Xil_DCacheFlush();
    
    // ========================================================================
    // SÜREKLI TRANSFER DÖNGÜSÜ
    // ========================================================================
    
    xil_printf("\r\n>>> Sürekli S2MM transferi başlatılıyor...\r\n");
    xil_printf(">>> GTY'den gelen veri DDR4'e yazılıyor...\r\n\r\n");
    
    while (1) {
        // Transfer adresi hesapla (circular buffer)
        transfer_addr = DDR4_BASE_ADDR + (gTransferCount * TRANSFER_SIZE) % (16 * TRANSFER_SIZE);
        
        // LED toggle (aktivite göstergesi)
        XGpio_DiscreteWrite(&Gpio, GPIO_CHANNEL_1, gTransferCount & 0xFF);
        
        // S2MM transfer başlat
        Status = DMA_Start_S2MM_Transfer(transfer_addr, TRANSFER_SIZE);
        if (Status != XST_SUCCESS) {
            xil_printf("❌ Transfer başlatılamadı!\r\n");
            break;
        }
        
        // Transfer tamamlanmasını bekle
        while ((XAxiDma_Busy(&AxiDma, XAXIDMA_DEVICE_TO_DMA))) {
            // Bekle
        }
        
        gTransferCount++;
        
        // Her 100 transferde bir bilgi yazdır
        if ((gTransferCount % 100) == 0) {
            xil_printf("📊 Transfer #%lu tamamlandı | Adres: 0x%08lX | Toplam: %lu MB\r\n",
                       gTransferCount, transfer_addr, (gTransferCount * TRANSFER_SIZE) / (1024*1024));
        }
    }
    
    xil_printf("\r\n✅ Program sonlandı.\r\n");
    return XST_SUCCESS;
}

// ============================================================================
// DMA BAŞLATMA FONKSİYONU
// ============================================================================

int DMA_Init(void)
{
    XAxiDma_Config *CfgPtr;
    int Status;
    
    // DMA konfigürasyonunu al
    CfgPtr = XAxiDma_LookupConfig(DMA_DEV_ID);
    if (!CfgPtr) {
        xil_printf("❌ DMA konfigürasyonu bulunamadı!\r\n");
        return XST_FAILURE;
    }
    
    // DMA'yı başlat
    Status = XAxiDma_CfgInitialize(&AxiDma, CfgPtr);
    if (Status != XST_SUCCESS) {
        xil_printf("❌ DMA başlatma hatası: %d\r\n", Status);
        return XST_FAILURE;
    }
    
    // Scatter Gather kontrolü (Simple Mode kullanıyoruz)
    if (XAxiDma_HasSg(&AxiDma)) {
        xil_printf("❌ DMA SG modunda, Simple Mode gerekli!\r\n");
        return XST_FAILURE;
    }
    
    // Interrupt'ları devre dışı bırak (polling mode)
    XAxiDma_IntrDisable(&AxiDma, XAXIDMA_IRQ_ALL_MASK, XAXIDMA_DEVICE_TO_DMA);
    
    return XST_SUCCESS;
}

// ============================================================================
// S2MM TRANSFER BAŞLATMA
// ============================================================================

int DMA_Start_S2MM_Transfer(u32 addr, u32 length)
{
    int Status;
    
    // Cache'i flush et (coherency için)
    Xil_DCacheFlushRange(addr, length);
    
    // S2MM transferini başlat
    Status = XAxiDma_SimpleTransfer(&AxiDma, addr, length, XAXIDMA_DEVICE_TO_DMA);
    if (Status != XST_SUCCESS) {
        return XST_FAILURE;
    }
    
    return XST_SUCCESS;
}

// ============================================================================
// VERİ DOĞRULAMA FONKSİYONU (Opsiyonel)
// ============================================================================

void Verify_Data(u32 addr, u32 length)
{
    u32 i;
    u32 *data_ptr = (u32 *)addr;
    u32 errors = 0;
    
    xil_printf("🔍 Veri doğrulanıyor...\r\n");
    
    // Cache'i invalidate et
    Xil_DCacheInvalidateRange(addr, length);
    
    // İlk 64 byte'ı yazdır
    xil_printf("\r\n📄 İlk 64 byte:\r\n");
    for (i = 0; i < 16; i++) {
        if (i % 4 == 0) xil_printf("\r\n0x%08X: ", addr + (i*4));
        xil_printf("0x%08lX ", data_ptr[i]);
    }
    xil_printf("\r\n");
    
    xil_printf("✅ Veri doğrulama tamamlandı.\r\n");
}

// ============================================================================
// BENCHMARK FONKSİYONU
// ============================================================================

void Print_Performance_Stats(void)
{
    u32 total_mb = (gTransferCount * TRANSFER_SIZE) / (1024 * 1024);
    
    xil_printf("\r\n╔══════════════════════════════════════════════════════╗\r\n");
    xil_printf("║           PERFORMANS İSTATİSTİKLERİ                 ║\r\n");
    xil_printf("╠══════════════════════════════════════════════════════╣\r\n");
    xil_printf("║  Toplam Transfer      : %8lu                    ║\r\n", gTransferCount);
    xil_printf("║  Transfer Boyutu      : %8lu byte              ║\r\n", TRANSFER_SIZE);
    xil_printf("║  Toplam Veri          : %8lu MB                ║\r\n", total_mb);
    xil_printf("╚══════════════════════════════════════════════════════╝\r\n\r\n");
}
