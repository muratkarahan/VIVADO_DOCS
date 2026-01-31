# DocNav TLS Hatası Çözümü

## Sorun

AMD Adaptive Computing Documentation Navigator (DocNav) açılırken şu hata mesajı çıkıyordu:

```
Failed to download ipdoc_coreswap.xml. An error occurred accessing the web site for catalog information:
"TLS initialization failed"
```

## Temel Neden

DocNav, **OpenSSL 1.0.2q** (2018) sürümünü kullanıyor. Bu sürüm:
- Modern TLS 1.3 desteklemiyor
- Güncel sunucu sertifika zincirleriyle uyumsuz
- AMD/Xilinx sunucularıyla TLS el sıkışması yapamıyor

---

## Denenen Yöntemler ve Sonuçları

### ❌ 1. Windows TLS Ayarları (Başarısız)

**Denenen:** Internet Options → Advanced → TLS 1.0, 1.1, 1.2, 1.3 etkinleştirme

```powershell
# Registry'den TLS ayarları kontrol edildi
Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client'
```

**Sonuç:** TLS zaten etkin, DocNav kendi OpenSSL kütüphanesini kullandığı için Windows ayarları etkisiz.

---

### ❌ 2. SSL Cache Temizleme (Başarısız)

**Denenen:** Windows SSL önbelleğini temizleme

```powershell
certutil -URLCache * delete
```

**Sonuç:** Etkisiz - sorun cache değil, kütüphane uyumsuzluğu.

---

### ❌ 3. SSL DLL'leri Devre Dışı Bırakma (Başarısız)

**Denenen:** DocNav'ın SSL DLL'lerini yeniden adlandırarak HTTPS'i devre dışı bırakma

```powershell
Rename-Item "C:\Xilinx\DocNav\libeay32.dll" "C:\Xilinx\DocNav\libeay32.dll.disabled"
Rename-Item "C:\Xilinx\DocNav\ssleay32.dll" "C:\Xilinx\DocNav\ssleay32.dll.disabled"
```

**Sonuç:** Aynı hata devam etti - DLL'ler başka yerden yüklenmiş olabilir veya Qt statik bağlı.

---

### ❌ 4. Qt Ortam Değişkenleri (Başarısız)

**Denenen:** Qt'nin TLS backend'ini Windows Schannel'a yönlendirme

```powershell
$env:QT_TLS_BACKEND = "schannel"
$env:QT_NETWORK_BACKEND = "native"
Start-Process "C:\Xilinx\DocNav\docnav.exe"
```

**Sonuç:** DocNav'ın Qt sürümü bu özelliği desteklemiyor.

---

### ❌ 5. CA Bundle ile Başlatma (Başarısız)

**Denenen:** Git'in CA bundle dosyasını OpenSSL'e gösterme

```powershell
$env:SSL_CERT_FILE = "C:\Program Files\Git\mingw64\etc\ssl\certs\ca-bundle.crt"
$env:SSL_CERT_DIR = ""
$env:OPENSSL_CONF = ""
Start-Process "C:\Xilinx\DocNav\docnav.exe"
```

**Sonuç:** Etkisiz - sorun sertifika değil, OpenSSL sürümü.

---

### ❌ 6. Windows Firewall ile Engelleme (Başarısız)

**Denenen:** DocNav'ın internet erişimini engelleyerek TLS denemesini önleme

```powershell
Start-Process powershell -ArgumentList '-Command "netsh advfirewall firewall add rule name=\"Block DocNav Internet\" dir=out program=\"C:\Xilinx\DocNav\docnav.exe\" action=block"' -Verb RunAs
```

**Sonuç:** Kural eklendi ama DocNav yine de hata penceresi gösterdi (açılışta kontrol yapıyor).

---

### ❌ 7. Sistemdeki Diğer OpenSSL DLL'leri (Başarısız)

**Denenen:** iOS SDK veya diğer programlardan libeay32.dll kopyalama

```powershell
# Sistemde mevcut libeay32.dll dosyaları arandı
Get-ChildItem -Path "C:\Program Files" -Recurse -Filter "libeay32.dll"
```

**Sonuç:** Bulunan DLL'ler de 1.0.2x serisiydi - aynı sorun.

---

### ✅ 8. OpenSSL 1.1.1w Kurulumu (BAŞARILI!)

**Analiz:**
```powershell
# DocNav DLL'lerinin PE header'ı kontrol edildi
# docnav.exe = x64 (0x8664)
# libeay32.dll = x64 (0x8664) 
# ssleay32.dll = x64 (0x8664)

# OpenSSL sürümü kontrol edildi
(Get-Item 'C:\Xilinx\DocNav\ssleay32.dll').VersionInfo
# FileVersion: 1.0.2q (2018 - ESKİ!)
```

**Çözüm:**
1. OpenSSL 1.1.1w (Win64) indirildi ve kuruldu
2. Yeni DLL'ler eski isimlerle DocNav'a kopyalandı:
   - `libcrypto-1_1-x64.dll` → `libeay32.dll`
   - `libssl-1_1-x64.dll` → `ssleay32.dll`

```powershell
# OpenSSL 1.1.1w indir
$url = "https://slproweb.com/download/Win64OpenSSL-1_1_1w.msi"
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\Win64OpenSSL-1_1_1w.msi"

# Kur (GUI ile)
Start-Process "$env:TEMP\Win64OpenSSL-1_1_1w.msi"

# DLL'leri değiştir
Stop-Process -Name docnav -Force -ErrorAction SilentlyContinue
Copy-Item "C:\Xilinx\DocNav\libeay32.dll" "C:\Xilinx\DocNav\libeay32.dll.old" -Force
Copy-Item "C:\Xilinx\DocNav\ssleay32.dll" "C:\Xilinx\DocNav\ssleay32.dll.old" -Force
Copy-Item "C:\Program Files\OpenSSL-Win64\libcrypto-1_1-x64.dll" "C:\Xilinx\DocNav\libeay32.dll" -Force
Copy-Item "C:\Program Files\OpenSSL-Win64\libssl-1_1-x64.dll" "C:\Xilinx\DocNav\ssleay32.dll" -Force

# Başlat
Start-Process "C:\Xilinx\DocNav\docnav.exe"
```

**Sonuç:** ✅ TLS hatası çözüldü, DocNav katalog güncellemesi yapabiliyor!

---

## Neden Bu Çözüm Çalıştı?

1. **DLL İsimleri Uyumlu:** OpenSSL 1.0.x ve 1.1.x aynı API'yi kullanıyor, sadece isimler farklı:
   - 1.0.x: `libeay32.dll`, `ssleay32.dll`
   - 1.1.x: `libcrypto-1_1-x64.dll`, `libssl-1_1-x64.dll`

2. **ABI Uyumluluğu:** OpenSSL 1.1.x, 1.0.x ile büyük ölçüde geriye uyumlu

3. **TLS 1.3 Desteği:** 1.1.1 serisi modern cipher suite'leri ve TLS 1.3'ü destekliyor

4. **x64 Mimari:** Hem DocNav hem de yeni DLL'ler 64-bit

---

## Çalışan Çözüm

OpenSSL 1.1.1w DLL'lerini DocNav klasörüne kopyalamak.

### Adım 1: OpenSSL 1.1.1w İndir ve Kur

1. [slproweb.com](https://slproweb.com/products/Win32OpenSSL.html) adresinden **Win64 OpenSSL v1.1.1w** indir
2. Veya PowerShell ile:
   ```powershell
   $url = "https://slproweb.com/download/Win64OpenSSL-1_1_1w.msi"
   $out = "$env:TEMP\Win64OpenSSL-1_1_1w.msi"
   Invoke-WebRequest -Uri $url -OutFile $out
   Start-Process $out
   ```
3. Kurulumu tamamla (varsayılan konum: `C:\Program Files\OpenSSL-Win64`)

### Adım 2: DocNav'ı Kapat

```powershell
Stop-Process -Name docnav -Force -ErrorAction SilentlyContinue
```

### Adım 3: Eski DLL'leri Yedekle

```powershell
Copy-Item "C:\Xilinx\DocNav\libeay32.dll" "C:\Xilinx\DocNav\libeay32.dll.old" -Force
Copy-Item "C:\Xilinx\DocNav\ssleay32.dll" "C:\Xilinx\DocNav\ssleay32.dll.old" -Force
```

### Adım 4: Yeni DLL'leri Kopyala

```powershell
Copy-Item "C:\Program Files\OpenSSL-Win64\libcrypto-1_1-x64.dll" "C:\Xilinx\DocNav\libeay32.dll" -Force
Copy-Item "C:\Program Files\OpenSSL-Win64\libssl-1_1-x64.dll" "C:\Xilinx\DocNav\ssleay32.dll" -Force
```

### Adım 5: DocNav'ı Başlat

```powershell
Start-Process "C:\Xilinx\DocNav\docnav.exe"
```

## Tek Komutla Çözüm

Tüm adımları tek seferde çalıştırmak için:

```powershell
# DocNav TLS Fix Script
Stop-Process -Name docnav -Force -ErrorAction SilentlyContinue
Start-Sleep 1

# Yedekle
Copy-Item "C:\Xilinx\DocNav\libeay32.dll" "C:\Xilinx\DocNav\libeay32.dll.old" -Force
Copy-Item "C:\Xilinx\DocNav\ssleay32.dll" "C:\Xilinx\DocNav\ssleay32.dll.old" -Force

# Yeni DLL'leri kopyala
Copy-Item "C:\Program Files\OpenSSL-Win64\libcrypto-1_1-x64.dll" "C:\Xilinx\DocNav\libeay32.dll" -Force
Copy-Item "C:\Program Files\OpenSSL-Win64\libssl-1_1-x64.dll" "C:\Xilinx\DocNav\ssleay32.dll" -Force

# Başlat
Start-Process "C:\Xilinx\DocNav\docnav.exe"
Write-Host "DocNav TLS fix uygulandı!"
```

## Geri Alma

Eğer sorun çıkarsa eski DLL'lere dönmek için:

```powershell
Stop-Process -Name docnav -Force -ErrorAction SilentlyContinue
Copy-Item "C:\Xilinx\DocNav\libeay32.dll.old" "C:\Xilinx\DocNav\libeay32.dll" -Force
Copy-Item "C:\Xilinx\DocNav\ssleay32.dll.old" "C:\Xilinx\DocNav\ssleay32.dll" -Force
Start-Process "C:\Xilinx\DocNav\docnav.exe"
```

## Teknik Detaylar

| Özellik | Eski (Sorunlu) | Yeni (Çözüm) |
|---------|----------------|--------------|
| OpenSSL Sürümü | 1.0.2q (2018) | 1.1.1w (2023) |
| TLS 1.2 | ✅ | ✅ |
| TLS 1.3 | ❌ | ✅ |
| Modern Cipher Suites | ❌ | ✅ |
| libeay32.dll Boyutu | 2.2 MB | 3.4 MB |
| ssleay32.dll Boyutu | 386 KB | 686 KB |

## Notlar

- Bu çözüm Vivado 2025.1 ile gelen DocNav için test edilmiştir
- DocNav güncellemesi DLL'leri eski sürüme çevirebilir, bu durumda işlemi tekrarlayın
- OpenSSL 1.1.1 serisi Eylül 2023'te EOL (End of Life) oldu ama hâlâ çalışıyor
- Kalıcı çözüm için AMD'nin DocNav'ı güncellemesi gerekiyor

## İlgili Dosyalar

- `start_docnav_tls_fix.bat` - CA bundle ile DocNav başlatma scripti
- `start_docnav_tls_debug.bat` - Debug modunda başlatma scripti
- `docnav_cli.ps1` - DocNav CLI aracı (GUI alternatifi)

---

## Bonus: DocNav CLI Aracı

TLS sorunu çözüldükten sonra, DocNav GUI'ye alternatif olarak komut satırından kullanılabilecek bir CLI aracı oluşturuldu.

### Özellikler

| Komut | Açıklama | Sonuç |
|-------|----------|-------|
| `-Search "AXI DMA"` | Dokümanlarda arama | ✅ 7 sonuç bulundu |
| `-Search "Zynq UltraScale"` | Geniş arama | ✅ 100+ sonuç |
| `-Categories` | Tüm kategorileri listele | ✅ 27 kategori, 9000+ doküman |
| `-Download PG021` | PDF indir | ✅ `downloaded_docs/PG021.pdf` |
| `-Open UG585` | Dokümanı aç (local veya web) | ✅ Çalışıyor |
| `-List` | Tüm dokümanları listele | ✅ Çalışıyor |
| `-List -Category "Versal"` | Kategoriye göre filtrele | ✅ Çalışıyor |

### Kullanım

```powershell
# Yardım
.\docnav_cli.ps1 -Help

# Arama
.\docnav_cli.ps1 -Search "AXI DMA"
.\docnav_cli.ps1 -Search "Zynq"

# Kategorileri görüntüle
.\docnav_cli.ps1 -Categories

# Kategoriye göre listele
.\docnav_cli.ps1 -List -Category "Versal"

# PDF indir
.\docnav_cli.ps1 -Download UG1304

# Dokümanı aç (local varsa local, yoksa web)
.\docnav_cli.ps1 -Open UG585
```

### Örnek Çıktılar

**Kategori Listesi:**
```
Kategori                 Doküman Sayısı
--------                 --------------
IP                                 2636
Vivado Design Suite                2352
7 Series                            560
Versal                              392
UltraScale                          376
Vitis                               365
Zynq 7000                           361
...
```

**Arama Sonucu (AXI DMA):**
```
DocID  Title                                            Category
-----  -----                                            --------
DS781  LogiCORE IP AXI DMA v7.1 Product Guide           IP
PG021  LogiCORE IP DMA v7.1 Product Guide (AXI)         IP
PG034  LogiCORE IP AXI CDMA v4.1 Product Guide          IP
...
```

### Teknik Detaylar

CLI aracı şu şekilde çalışıyor:

1. **Katalog Okuma:** `C:\Xilinx\DocNav\resources\xdocs.xml` dosyasını parse eder
2. **XML Yapısı:** `collection > catalog > group > document` hiyerarşisi
3. **Arama:** Regex ile DocID, Title, Tooltip ve Category alanlarında arar
4. **İndirme:** `downloadURL` alanından doğrudan PDF indirir
5. **Açma:** Önce local dosya kontrol eder, yoksa `webLocation` URL'ini açar

---

## Tarih

- **Çözüm Tarihi:** 31 Ocak 2026
- **Test Edilen Sistem:** Windows 11, Vivado 2025.1, DocNav 2025.05.29
