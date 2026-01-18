# 🎯 VIVADO_DOCS Kurulum Rehberi

## 🚀 Hızlı Başlangıç

### 1. Repository'yi Klonlayın
```powershell
cd C:\Users\<username>\Documents\GitHub
git clone <VIVADO_DOCS_URL>
cd VIVADO_DOCS
```

### 2. Virtual Environment Oluşturun
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Paketleri Yükleyin
```powershell
pip install -r ai_assistant/requirements.txt
```

### 4. OpenAI API Key Ayarlayın
```powershell
# Ortam değişkeni
$env:OPENAI_API_KEY = "sk-proj-..."

# veya .env dosyası
echo OPENAI_API_KEY=sk-proj-... > .env
```

### 5. Vivado Dökümanlarını İndirin
- Xilinx Documentation Portal'dan gerekli PDF'leri indirin
- `official_docs/` klasörüne yerleştirin
- Detaylar: [official_docs/README.md](official_docs/README.md)

### 6. Dökümanları İndexleyin
```powershell
cd ai_assistant
python setup_vivado_ai.py
```

### 7. VS Code Extension'ı Derleyin
```powershell
cd ai_assistant/vscode-extension
npm install
npm run compile
```

### 8. Extension'ı Test Edin
- VS Code'da `VIVADO_DOCS.code-workspace` açın
- `F5` ile debug modda başlatın
- Chat'te `@vivado` yazın

---

## 📚 Döküman İndirme Listesi

### Zorunlu (Minimum Set):
- ✅ UG835 - Vivado TCL Command Reference
- ✅ UG994 - IP Integrator User Guide
- ✅ PG057 - AXI Interconnect
- ✅ PG058 - FIFO Generator
- ✅ UG585 - Zynq-7000 TRM (Zynq kullanıyorsanız)

### Tavsiye Edilen:
- UG901 - Synthesis
- UG904 - Implementation
- UG906 - Design Analysis and Closure
- UG949 - UltraFast Methodology
- PG080 - AXI DMA

---

## 🧪 Test

```powershell
# Demo script
python ai_assistant/demo.py

# Manuel agent
python ai_assistant/vivado_agent.py
```

---

## ❓ Sorun Giderme

### ChromaDB hatası:
```powershell
pip install --upgrade chromadb
```

### OpenAI API hatası:
```powershell
# API key kontrolü
echo $env:OPENAI_API_KEY
```

### Extension derleme hatası:
```powershell
cd ai_assistant/vscode-extension
npm install --force
npm run compile
```

---

## 📞 Yardım

GitHub Issues veya Discussions kullanın.
