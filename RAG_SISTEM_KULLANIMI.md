# 🚀 RAG Sistemi Hızlı Başlatma Kılavuzu

## VIVADO_DOCS için RAG Sistemi

### Adım 1: Vivado Dökümanlarını İndirin

**Gerekli Minimum Set:**

1. **UG835** - Vivado TCL Command Reference
   - https://docs.xilinx.com/r/en-US/ug835-vivado-tcl-commands

2. **UG994** - IP Integrator User Guide
   - https://docs.xilinx.com/r/en-US/ug994-vivado-ip-subsystems

3. **PG057** - AXI Interconnect
   - https://docs.xilinx.com/r/en-US/pg057-axi-interconnect

4. **PG058** - FIFO Generator
   - https://docs.xilinx.com/r/en-US/pg058-fifo-generator

5. **UG585** - Zynq-7000 TRM (Zynq kullanıyorsanız)
   - https://docs.xilinx.com/r/en-US/ug585-zynq-7000-SoC-TRM

**İndirme:**
- Xilinx Documentation Portal: https://www.xilinx.com/support/documentation.html
- PDF'leri şu klasörlere yerleştirin:
  - `VIVADO_DOCS/official_docs/Design_Tools/` → UG'ler
  - `VIVADO_DOCS/official_docs/IP_Cores/` → PG'ler

### Adım 2: Environment Hazırla
```powershell
cd C:\Users\murat\Documents\GitHub\VIVADO_DOCS

# Virtual environment oluştur
python -m venv venv
.\venv\Scripts\Activate.ps1

# Paketleri yükle
pip install -r ai_assistant/requirements.txt
```

### Adım 3: OpenAI API Key Ayarla
```powershell
# Ortam değişkeni
$env:OPENAI_API_KEY = "sk-proj-..."

# veya .env dosyası
echo OPENAI_API_KEY=sk-proj-... > .env
```

### Adım 4: Dökümanları İndexleyin
```powershell
cd ai_assistant
python setup_vivado_ai.py
```

**Beklenen Çıktı:**
```
📚 VIVADO DÖKÜMAN İNDEXLEME
====================================
📁 XX PDF dosyası bulundu
📄 UG835.pdf
   Sayfa sayısı: XXX
   ✅ XXX chunk eklendi
...
📊 İNDEXLEME TAMAMLANDI
✅ Başarılı: XX/XX PDF
📝 Toplam chunk: XXXX
💾 Database: ./vivado_vectordb
```

### Adım 5: RAG Agent'ı Başlatın
```powershell
python vivado_agent.py
```

**Menü:**
- 1 → İnteraktif Chat Modu (ÖNERİLEN)
- 2 → Tek Soru-Cevap

### Adım 6: Örnek Sorular

```
# Temel soru
AXI4-Lite nedir?

# Kod isteği
AXI4-Lite master interface Verilog kodu yaz

# Döküman arama
IP Integrator'da block design nasıl oluşturulur?

# Karmaşık soru
Zynq PS ile PL arasında DMA kullanarak veri transferi nasıl yapılır?
```

---

## 🎯 Demo Script ile Test

```powershell
cd C:\Users\murat\Documents\GitHub\VIVADO_DOCS\ai_assistant
python demo.py
```

---

## 📊 ChromaDB Durum Kontrolü

```powershell
cd ai_assistant
python
```
```python
import chromadb
client = chromadb.PersistentClient(path="./vivado_vectordb")
collection = client.get_collection(name="vivado_docs")
print(f"Toplam döküman chunk: {collection.count()}")
```

---

## 🔧 Sorun Giderme

### OpenAI API Key Hatası
```powershell
echo OPENAI_API_KEY=sk-proj-... > .env
```

### ChromaDB Hatası
```powershell
pip install --upgrade chromadb
```

### Yeniden İndexleme
```powershell
python setup_vivado_ai.py --reindex
```

---

🚀 **RAG sistemi kullanıma hazır!**
