# Vivado FPGA Expert - VS Code Chat Participant Kurulum

## 📦 Gereksinimler

### Python Bağımlılıkları
```bash
cd ai_assistant
pip install flask flask-cors python-dotenv openai chromadb
```

### Node.js Bağımlılıkları  
```bash
cd ai_assistant/vscode-extension
npm install
```

## 🚀 Hızlı Başlangıç

### 1. MCP Server'ı Başlat

Terminal 1:
```powershell
cd C:\Users\murat\Documents\GitHub\VIVADO_DOCS\ai_assistant
python vivado_mcp_server.py
```

Çıktı:
```
================================================================================
🚀 Vivado FPGA Expert - MCP Server
================================================================================
📚 RAG Database: 2127 doküman
🤖 Model: GPT-4
🌐 Server: http://localhost:5000
================================================================================

✅ Server hazır! VS Code'dan @vivado ile kullanabilirsiniz.
```

### 2. VS Code Extension'ı Yükle

Terminal 2:
```powershell
cd C:\Users\murat\Documents\GitHub\VIVADO_DOCS\ai_assistant\vscode-extension

# TypeScript compile
npm run compile

# Extension'ı test et (Development Host açılır)
code --extensionDevelopmentPath=.
```

### 3. VS Code Chat'te Kullan

Yeni açılan VS Code penceresinde:

1. **Chat panelini** aç: `Ctrl+Shift+I` veya View → Chat
2. Chat'e **`@vivado`** yaz
3. Sorunu sor!

## 💬 Kullanım Örnekleri

### Genel Sorular
```
@vivado AXI4-Lite nedir?
@vivado Zynq PS ile PL arasında nasıl iletişim kurulur?
@vivado DDR4 controller nasıl konfigüre edilir?
```

### Komutlar

#### `/search` - Döküman ara
```
@vivado /search AXI DMA Product Guide
@vivado /search UG1144 Zynq UltraScale+
```

#### `/code` - Kod örneği al
```
@vivado /code AXI4-Lite slave Verilog
@vivado /code create_bd_cell TCL script
@vivado /code AXI DMA S2MM transfer C code
```

#### `/explain` - Kavram açıkla
```
@vivado /explain AXI interconnect
@vivado /explain GTY transceiver
@vivado /explain MIG DDR4
```

#### `/debug` - Hata ayıkla
```
@vivado /debug timing violation
@vivado /debug AXI protocol error
@vivado /debug synthesis failing
```

## 🔧 Konfigürasyon

VS Code Settings (`Ctrl+,`):

```json
{
  "vivadoExpert.pythonPath": "python",
  "vivadoExpert.ragScriptPath": "${workspaceFolder}/ai_assistant/vivado_mcp_server.py",
  "vivadoExpert.autoStart": true,
  "vivadoExpert.vivadoVersion": "2023.2",
  "vivadoExpert.enableTCLSuggestions": true
}
```

## 🌐 MCP Server API

### Health Check
```bash
curl http://localhost:5000/health
```

Yanıt:
```json
{
  "status": "healthy",
  "collection_size": 2127,
  "model": "gpt-4"
}
```

### Query Endpoint
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AXI4-Lite nedir?",
    "command": "explain",
    "n_results": 5
  }'
```

Yanıt:
```json
{
  "success": true,
  "answer": "AXI4-Lite hafif bir protocol...",
  "contexts": [
    {
      "content": "...",
      "source": "xilinx_vivado",
      "file": "ug1144.md",
      "relevance": 0.95
    }
  ],
  "tokens": 1234
}
```

### Search Endpoint (GPT'siz)
```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AXI DMA",
    "n_results": 10
  }'
```

### Stats Endpoint
```bash
curl http://localhost:5000/stats
```

Yanıt:
```json
{
  "total_documents": 2127,
  "sources": {
    "vivado_verilog_templates": 572,
    "markdown_docs": 429,
    "docs_fpga": 264
  },
  "database_path": "vivado_vectordb_full"
}
```

## 🛠️ Geliştirme

### Extension Debug

1. VS Code'da `vscode-extension` klasörünü aç
2. `F5` bas (Debug başlar)
3. Yeni pencere açılır - Extension Host
4. Chat panelinde `@vivado` test et

### Extension Build & Package

```bash
# TypeScript compile
npm run compile

# VSIX package oluştur
npm install -g vsce
vsce package

# Çıktı: vivado-fpga-expert-1.0.0.vsix
```

### Extension Yükle

```bash
code --install-extension vivado-fpga-expert-1.0.0.vsix
```

## 📊 Performans

- **İlk yanıt süresi:** 2-5 saniye
- **RAG arama:** <500ms
- **GPT-4 yanıt:** 2-4 saniye
- **Toplam token:** 500-2000/sorgu
- **Maliyet:** ~$0.01-0.04/sorgu

## 🔐 Güvenlik

- `.env` dosyası `.gitignore`'da
- API key'ler lokal tutulur
- MCP server sadece localhost'tan erişilebilir
- CORS sadece gerekirse aktif

## 🐛 Sorun Giderme

### Server başlamıyor
```bash
# Port kullanımda mı?
netstat -ano | findstr :5000

# Python bağımlılıkları eksik mi?
pip install -r requirements.txt
```

### Extension görünmüyor
```bash
# Extension listesini kontrol et
code --list-extensions | findstr vivado

# Log'lara bak
# View → Output → Vivado Expert
```

### RAG yanıt vermiyor
```bash
# ChromaDB kontrolü
python -c "import chromadb; print(chromadb.__version__)"

# Collection kontrolü
cd ai_assistant
python
>>> import chromadb
>>> client = chromadb.PersistentClient(path="./vivado_vectordb_full")
>>> coll = client.get_collection("vivado_full_system")
>>> print(coll.count())
```

## 📚 Ek Kaynaklar

- [VS Code Chat API](https://code.visualstudio.com/api/extension-guides/chat)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [Flask REST API](https://flask.palletsprojects.com/)

## 🤝 Katkıda Bulunma

Extension geliştirmeleri için:
1. `vscode-extension/src/extension.ts` düzenle
2. `npm run compile` çalıştır
3. `F5` ile test et

MCP Server geliştirmeleri için:
1. `vivado_mcp_server.py` düzenle
2. Server'ı restart et
3. API endpoint'lerini test et

## 📄 Lisans

Bu proje eğitim amaçlıdır. OpenAI API kullanımı için geçerli lisans koşulları geçerlidir.

---

**Son Güncelleme:** 18 Ocak 2026
**VS Code Versiyonu:** 1.85+
**Python Versiyonu:** 3.8+
