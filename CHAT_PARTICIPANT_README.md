# Vivado FPGA Expert - VS Code Chat Participant

VS Code içinde **inline chat** yapabileceğiniz, RAG destekli Vivado FPGA asistanı!

## ✨ Özellikler

- 🤖 **@vivado** chat participant (Copilot benzeri)
- 📚 **2,127 doküman** RAG database (Vivado, Verilog, VHDL, TCL)
- 💬 **GPT-4** ile context-aware yanıtlar
- ⚡ **Slash commands:** `/search`, `/code`, `/explain`, `/debug`
- 🔗 **MCP Server** backend (Python Flask)
- 📖 **Kaynak referansları** her yanıtta

## 🚀 Hızlı Başlangıç

### 1. MCP Server'ı Başlat

#### Windows:
```cmd
start_vivado_mcp.bat
```

#### Manuel:
```powershell
cd ai_assistant
python vivado_mcp_server.py
```

Çıktı:
```
✅ RAG Collection yüklendi: 2127 doküman
🌐 Server: http://localhost:5000
✅ Server hazır! VS Code'dan @vivado ile kullanabilirsiniz.
```

### 2. VS Code Extension'ı Yükle

```bash
cd ai_assistant/vscode-extension
npm install
npm run compile

# Extension'ı test et
code --extensionDevelopmentPath=.
```

### 3. Chat'te Kullan

VS Code'da:
1. Chat panelini aç: `Ctrl+Shift+I`
2. **`@vivado`** yaz
3. Soruyu sor!

## 💡 Örnek Kullanımlar

### Genel Sorular
```
@vivado AXI4-Lite nedir ve nasıl kullanılır?
@vivado Zynq PS ile PL nasıl haberleşir?
@vivado DDR4 MIG konfigürasyonu nasıl yapılır?
```

### Slash Commands

**`/search`** - Döküman ara
```
@vivado /search AXI DMA Product Guide
@vivado /search GTY transceiver UG
```

**`/code`** - Kod örneği
```
@vivado /code AXI4-Lite slave Verilog örneği
@vivado /code create_bd_cell TCL script
@vivado /code AXI DMA C kodu
```

**`/explain`** - Kavram açıkla
```
@vivado /explain AXI interconnect
@vivado /explain clock domain crossing
```

**`/debug`** - Hata ayıkla
```
@vivado /debug timing violation nasıl çözülür
@vivado /debug AXI protocol error
```

## 📦 Dosya Yapısı

```
VIVADO_DOCS/
├── start_vivado_mcp.bat           # MCP server başlatma scripti
├── ai_assistant/
│   ├── vivado_mcp_server.py       # Backend API server
│   ├── vivado_vectordb_full/      # ChromaDB database (2127 docs)
│   └── vscode-extension/
│       ├── package.json           # Extension manifest
│       ├── src/extension.ts       # Chat participant kodu
│       └── SETUP_GUIDE.md         # Detaylı kurulum
└── virtex7_gty_dma_ddr4/          # Örnek tasarım
```

## 🔧 Konfigürasyon

VS Code Settings (`settings.json`):
```json
{
  "vivadoExpert.pythonPath": "python",
  "vivadoExpert.autoStart": true,
  "vivadoExpert.vivadoVersion": "2023.2"
}
```

## 🌐 API Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

### Query (GPT-4)
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"AXI4 nedir?","command":"explain"}'
```

### Search (RAG Only)
```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"DDR4","n_results":10}'
```

### Stats
```bash
curl http://localhost:5000/stats
```

## 📊 RAG Database İçeriği

- **Toplam:** 2,127 chunk
- **Kaynaklar:**
  - Vivado Verilog templates: 572
  - Markdown docs: 429
  - FPGA docs: 264
  - Project examples: 161
  - IP core docs: 84
  - Official guides: 82

## 🎯 Chat Participant Özellikleri

### Akıllı Context
- Önceki mesajları hatırlar
- Projeye özel öneriler
- Kod snippet'leri clipboard'a kopyalar

### Slash Commands
- `/search` - Spesifik döküman ara
- `/code` - Çalışan kod örneği
- `/explain` - Detaylı açıklama
- `/debug` - Hata çözüm önerileri

### Kaynak Referansları
Her yanıtta:
- İlgili UG/PG numaraları
- Kaynak dosya isimleri
- Relevance score (uygunluk %)

## 🛠️ Geliştirme

### Extension Debug
```bash
cd ai_assistant/vscode-extension
code .
# F5 bas -> Extension Host açılır
```

### Server Debug
```bash
cd ai_assistant
python vivado_mcp_server.py
# Flask debug mode açık, otomatik reload
```

### Database Güncelleme
```bash
cd ai_assistant
python train_rag_full_system.py  # Yeni dokümanlar ekle
```

## 📚 Daha Fazla Bilgi

- **Kurulum Kılavuzu:** `ai_assistant/vscode-extension/SETUP_GUIDE.md`
- **RAG Eğitim:** `ai_assistant/RAG_TRAINING_GUIDE.md`
- **Örnek Tasarım:** `virtex7_gty_dma_ddr4/README.md`

## 🔐 Güvenlik

- `.env` dosyasında OpenAI API key
- Server sadece localhost (127.0.0.1:5000)
- CORS sadece gerekirse aktif
- Tüm veriler local

## 🐛 Sorun Giderme

**Server başlamıyor:**
```bash
pip install flask flask-cors
python vivado_mcp_server.py
```

**Extension görünmüyor:**
```bash
# Developer Tools'da log kontrol et
Ctrl+Shift+I -> Console
```

**RAG yanıt vermiyor:**
```bash
# Database kontrolü
curl http://localhost:5000/stats
```

## 📄 Lisans

Eğitim amaçlı. OpenAI API kullanımı için geçerli lisans koşulları geçerlidir.

---

**Oluşturulma:** 18 Ocak 2026  
**VS Code:** 1.85+  
**Python:** 3.8+  
**Model:** GPT-4
