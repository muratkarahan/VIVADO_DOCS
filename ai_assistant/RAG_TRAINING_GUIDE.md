# 🚀 Vivado FPGA Expert - RAG Eğitim Kılavuzu

Bu kılavuz, workspace'inizdeki tüm Vivado ve FPGA Xilinx dokümanlarından RAG (Retrieval-Augmented Generation) sistemi nasıl oluşturulacağını adım adım açıklar.

## 📋 İçindekiler

1. [Gereksinimler](#gereksinimler)
2. [Kurulum](#kurulum)
3. [RAG Eğitimi](#rag-egitimi)
4. [AI Asistanı Kullanma](#ai-asistani-kullanma)
5. [İleri Seviye Kullanım](#ileri-seviye-kullanim)
6. [Sorun Giderme](#sorun-giderme)

---

## 🔧 Gereksinimler

### Yazılım Gereksinimleri
- **Python 3.8+** (Python 3.10 önerilir)
- **pip** (Python paket yöneticisi)
- **OpenAI API Key** ([buradan alın](https://platform.openai.com/api-keys))

### Sistem Gereksinimleri
- **RAM:** En az 4GB (8GB önerilir)
- **Disk:** En az 2GB boş alan (vector database için)
- **İnternet:** API çağrıları ve paket indirme için

---

## 📦 Kurulum

### Adım 1: Python Ortamını Hazırlayın

```powershell
# ai_assistant klasörüne gidin
cd c:\Users\murat\Documents\GitHub\VIVADO_DOCS\ai_assistant

# Virtual environment oluşturun (önerilir)
python -m venv venv

# Virtual environment'ı aktifleştirin
.\venv\Scripts\activate
```

### Adım 2: Gerekli Paketleri Yükleyin

```powershell
# Tüm gereksinimleri yükleyin
pip install -r requirements.txt

# Veya minimal kurulum (sadece temel özellikler)
pip install openai chromadb tiktoken python-dotenv PyPDF2 tqdm
```

### Adım 3: OpenAI API Key Ayarlayın

1. `.env.example` dosyasını kopyalayıp `.env` adıyla kaydedin:
```powershell
copy .env.example .env
```

2. `.env` dosyasını düzenleyin ve API key'inizi ekleyin:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

---

## 🎓 RAG Eğitimi

### Otomatik Eğitim (Önerilen)

Tüm workspace'deki dokümanları (MD, PDF, TXT) otomatik olarak işler:

```powershell
# Tüm dokümanları işle ve vector database oluştur
python train_rag_complete.py

# Collection'ı sıfırdan oluştur (varsa eskiyi sil)
python train_rag_complete.py --reindex

# Eğitim sonrası otomatik test yap
python train_rag_complete.py --test
```

### Manuel Eğitim (Sadece PDF'ler)

Eğer sadece `official_docs/` klasöründeki PDF'leri işlemek isterseniz:

```powershell
python setup_vivado_ai.py

# Reindex
python setup_vivado_ai.py --reindex
```

### Eğitim Süreci

Script çalıştırıldığında şu adımlar gerçekleşir:

1. **📁 Dosya Tarama:** Workspace'de tüm `.md`, `.pdf`, `.txt` dosyaları bulunur
2. **📝 Metin Çıkarma:** Her dosyadan metin içeriği çıkarılır
3. **✂️ Chunking:** Metinler akıllı şekilde 1000 token'lık parçalara bölünür
4. **🔢 Embedding:** Her chunk için OpenAI embeddings oluşturulur
5. **💾 Database:** ChromaDB vector database'e kaydedilir

**Örnek Çıktı:**
```
================================================================================
🚀 VIVADO RAG TAM EĞİTİM SİSTEMİ
================================================================================
📂 Workspace: c:\Users\murat\Documents\GitHub\VIVADO_DOCS
💾 Database: ./vivado_vectordb

🔍 Dosyalar taranıyor...

📊 Bulunan Dosyalar:
   📝 Markdown: 6
   📄 PDF: 0
   📄 Text: 0
   📚 Toplam: 6

--------------------------------------------------------------------------------
📝 MARKDOWN DOSYALARI İŞLENİYOR
--------------------------------------------------------------------------------

📝 README.md
   ✅ 45 chunk eklendi

📝 KURULUM.md
   ✅ 23 chunk eklendi

...

================================================================================
✅ RAG EĞİTİMİ TAMAMLANDI
================================================================================

📊 İstatistikler:
   ⏱️  Süre: 12.4 saniye
   📝 Markdown: 6 dosya
   📄 PDF: 0 dosya
   📄 Text: 0 dosya
   📚 Toplam Chunk: 234
   🔢 Toplam Token: 45,123
   💾 Database: 234 döküman
   💰 Tahmini Embedding Maliyet: $0.0045
================================================================================
```

---

## 🤖 AI Asistanı Kullanma

### İnteraktif Chat Modu

```powershell
python vivado_agent.py
```

Menüden **1** seçerek interaktif chat başlatın:

```
👤 Siz: Vivado'da AXI4-Lite interface nasıl oluşturulur?

🔍 Dökümanlar aranıyor...
📚 5 döküman bulundu
🤖 AI düşünüyor...

================================================================================
💬 CEVAP:
================================================================================
AXI4-Lite interface oluşturmak için şu adımları izleyebilirsiniz:

1. **IP Integrator Kullanımı:**
   - Vivado'da IP Integrator açın (Create Block Design)
   - Add IP butonuna tıklayın
   - "AXI" araması yapın
   - İhtiyacınıza göre IP seçin (örn: AXI GPIO, AXI BRAM Controller)

2. **Custom IP Oluşturma:**
   - Tools → Create and Package IP
   - Create AXI4 Peripheral seçin
   - Interface tipini AXI4-Lite seçin
   ...

[Kaynak: KURULUM.md, README.md]

--------------------------------------------------------------------------------
📊 Token Kullanımı: Input=1234, Output=456
💰 Bu sorgu maliyeti: $0.0234
💵 Toplam maliyet: $0.0234 (1 sorgu)
================================================================================
```

### Tek Soru-Cevap Modu

```powershell
python vivado_agent.py
# Menüden 2 seçin ve sorunuzu yazın
```

### Komutlar

Chat sırasında kullanabileceğiniz komutlar:

- **Normal metin:** Soru sorun
- **`stats`:** Maliyet istatistiklerini göster
- **`clear`:** Ekranı temizle
- **`quit` / `exit` / `q`:** Çıkış

---

## 🔍 İleri Seviye Kullanım

### Özel Workspace Klasörü

```powershell
python train_rag_complete.py --workspace "D:/MyVivadoDocs"
```

### Belirli Klasörleri Atlama

```powershell
python train_rag_complete.py --skip-patterns node_modules build dist
```

### ChromaDB Konumunu Değiştirme

```powershell
python train_rag_complete.py --db-path "D:/vectordb/vivado"
```

### Chunk Boyutunu Ayarlama

`train_rag_complete.py` dosyasında:

```python
# Satır ~75 civarı
chunks = self.chunk_text(text, chunk_size=1500, overlap=200)
```

- **chunk_size:** Daha büyük = daha fazla context, daha az chunk
- **overlap:** Chunk'lar arası örtüşme (continuity için)

### Vector Database Yedekleme

```powershell
# Database klasörünü kopyalayın
xcopy /E /I vivado_vectordb vivado_vectordb_backup
```

### Collection Silme

```python
# Python'da
import chromadb
client = chromadb.PersistentClient(path="./vivado_vectordb")
client.delete_collection("vivado_docs_complete")
```

---

## 🎯 PDF Dokümanları Ekleme

### 1. PDF'leri İndirin

Xilinx resmi sitesinden ([xilinx.com/support/documentation](https://www.xilinx.com/support/documentation.html)) PDF'leri indirin.

### 2. Klasörlere Yerleştirin

```
official_docs/
├── Design_Tools/       # UG835, UG892, UG893, vb.
├── IP_Cores/          # PG057, PG058, PG080, vb.
├── SoC_Embedded/      # UG585, UG1085, vb.
├── Transceivers/      # UG476, UG576, vb.
└── Datasheets/        # DS180, DS190, DS925, vb.
```

### 3. Reindex

```powershell
python train_rag_complete.py --reindex
```

**Önerilen Dökümanlar (Öncelik Sırasına Göre):**

1. **UG835** - Vivado Tcl Command Reference (~2000 sayfa)
2. **UG949** - UltraFast Design Methodology (~500 sayfa)
3. **UG994** - IP Integrator (~300 sayfa)
4. **UG585** - Zynq-7000 TRM (~1800 sayfa)
5. **PG057** - AXI Interconnect (~100 sayfa)

---

## 💰 Maliyet Tahmini

### Embedding Maliyeti (text-embedding-ada-002)

- **Fiyat:** $0.0001 / 1K token
- **Örnek:** 100,000 token = **$0.01**

### Chat Maliyeti (gpt-4-turbo-preview)

- **Input:** $0.01 / 1K token
- **Output:** $0.03 / 1K token
- **Örnek Sorgu:** 2K input + 500 output = **$0.035**

### Tahmini Toplam Maliyet

**İlk Eğitim:**
- 6 Markdown dosya (~50K token): $0.005
- 10 PDF dosya (~500K token): $0.050
- **Toplam:** ~$0.055

**Aylık Kullanım:**
- 100 soru (~300K token total): ~$10
- 500 soru (~1.5M token total): ~$50

---

## 📊 Performans Optimizasyonu

### 1. Chunk Size Ayarlama

**Küçük Chunks (500-800 token):**
- ✅ Daha hassas arama
- ✅ Daha az false positive
- ❌ Daha fazla chunk (daha pahalı)

**Büyük Chunks (1200-1500 token):**
- ✅ Daha fazla context
- ✅ Daha az chunk (daha ucuz)
- ❌ Daha az hassas arama

### 2. Search Results Sayısı

`vivado_agent.py` içinde:

```python
results = self.collection.query(
    query_texts=[query],
    n_results=5  # 3-7 arası önerilir
)
```

- **Daha az (3):** Daha hızlı, daha ucuz
- **Daha fazla (10):** Daha kapsamlı, daha pahalı

### 3. Model Seçimi

**gpt-4-turbo-preview:**
- ✅ En iyi kalite
- ❌ En pahalı

**gpt-3.5-turbo:**
- ✅ En ucuz
- ❌ Daha düşük kalite

Değiştirmek için `vivado_agent.py` içinde:

```python
model="gpt-3.5-turbo"  # Satır ~55 civarı
```

---

## 🐛 Sorun Giderme

### Problem: "OPENAI_API_KEY bulunamadı"

**Çözüm:**
```powershell
# .env dosyasının olduğundan emin olun
ls .env

# API key'in doğru formatta olduğunu kontrol edin
cat .env
```

### Problem: "Collection not found"

**Çözüm:**
```powershell
# Önce eğitim yapın
python train_rag_complete.py
```

### Problem: "PDF'ler işlenmiyor"

**Çözüm:**
```powershell
# PyPDF2'nin yüklü olduğundan emin olun
pip install PyPDF2 pypdf
```

### Problem: "ChromaDB hatası"

**Çözüm:**
```powershell
# ChromaDB'yi yeniden yükleyin
pip uninstall chromadb
pip install chromadb>=0.4.0

# Database klasörünü silin ve yeniden oluşturun
rm -r vivado_vectordb
python train_rag_complete.py
```

### Problem: "Out of Memory"

**Çözüm:**
- Chunk size'ı küçültün (800'e düşürün)
- PDF'leri batch batch işleyin
- Daha fazla RAM'e sahip makine kullanın

### Problem: "Rate Limit Exceeded"

**Çözüm:**
```python
# train_rag_complete.py içine delay ekleyin
import time
time.sleep(1)  # Her chunk sonrası 1 saniye bekle
```

---

## 📚 Ek Kaynaklar

### Doküman İndeksi

[OFFICIAL_DOCS_INDEX.md](../OFFICIAL_DOCS_INDEX.md) dosyasına bakın.

### Kod Örnekleri

[KOD_ORNEKLERI.md](../KOD_ORNEKLERI.md) dosyasında Vivado TCL, Verilog, VHDL örnekleri bulabilirsiniz.

### Demo Örnekleri

[DEMO_ORNEKLERI.md](../DEMO_ORNEKLERI.md) dosyasında hazır demo projeler vardır.

---

## 🎯 Sonraki Adımlar

1. ✅ **PDF dokümanları indirin ve ekleyin**
   - Xilinx sitesinden UG835, UG949, UG994 gibi temel kılavuzları indirin
   - `official_docs/` klasörüne yerleştirin
   - `python train_rag_complete.py --reindex` çalıştırın

2. ✅ **Sistemi test edin**
   - `python train_rag_complete.py --test` ile otomatik test
   - `python vivado_agent.py` ile manuel test

3. ✅ **Özelleştirin**
   - Chunk size ayarlayın
   - Model seçin (GPT-4 vs GPT-3.5)
   - Prompt'ları düzenleyin

4. ✅ **Üretimde kullanın**
   - Web interface ekleyin (Streamlit/Gradio)
   - API endpoint oluşturun (FastAPI)
   - VS Code extension geliştirin

---

## 🤝 Katkıda Bulunma

Bu projeye katkıda bulunmak için:

1. Issue açın (bug report, feature request)
2. Fork yapın ve geliştirin
3. Pull request gönderin

---

## 📄 Lisans

Bu proje MIT lisansı altındadır.

---

## 💡 İpuçları

- 🎯 **İyi Sorular Sorun:** "Vivado nedir?" yerine "Vivado'da timing constraint nasıl tanımlanır?" gibi spesifik sorular sorun
- 📚 **Kaynaklara Dikkat:** AI'ın hangi dokümanları kullandığını kontrol edin
- 💰 **Maliyeti İzleyin:** `stats` komutu ile token kullanımını takip edin
- 🔄 **Düzenli Güncelleme:** Yeni Vivado sürümleri çıktığında dokümanları güncelleyin
- 🧪 **Test Edin:** Önemli projeler için AI'ın cevaplarını resmi dokümanlarla doğrulayın

---

**🚀 Artık hazırsınız! İyi çalışmalar!**

Sorularınız için: [GitHub Issues](https://github.com/your-repo/issues)
