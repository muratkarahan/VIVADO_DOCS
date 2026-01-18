# 🚀 Hızlı Başlangıç - Vivado RAG Sistemi

5 dakikada RAG sisteminizi kurup çalıştırın!

## 📋 Ön Hazırlık

1. **Python 3.8+** yüklü olmalı
2. **OpenAI API Key** hazır olmalı ([buradan alın](https://platform.openai.com/api-keys))

## ⚡ Hızlı Kurulum

```powershell
# 1. Klasöre gidin
cd c:\Users\murat\Documents\GitHub\VIVADO_DOCS\ai_assistant

# 2. Virtual environment oluşturun (opsiyonel ama önerilir)
python -m venv venv
.\venv\Scripts\activate

# 3. Paketleri yükleyin
pip install -r requirements.txt

# 4. API Key ayarlayın
copy .env.example .env
# .env dosyasını açıp OPENAI_API_KEY değerini değiştirin

# 5. RAG eğitimi yapın (tüm MD, PDF, TXT dosyalarını işler)
python train_rag_complete.py

# 6. AI asistanı başlatın
python vivado_agent.py
```

## 🎯 İlk Soru

AI asistan çalıştıktan sonra şu sorulardan birini deneyin:

- "Vivado'da IP Integrator nasıl kullanılır?"
- "AXI4-Lite ve AXI4-Stream farkı nedir?"
- "Zynq PS-PL haberleşmesi nasıl yapılır?"
- "FPGA synthesis optimization teknikleri nelerdir?"
- "Vivado TCL scripting örnekleri ver"

## 📁 PDF Doküman Ekleme

Daha iyi sonuçlar için Xilinx PDF dokümanlarını ekleyin:

```powershell
# 1. PDF'leri xilinx.com'dan indirin
# 2. official_docs/ klasörüne yerleştirin:
#    - Design_Tools/UG835.pdf
#    - Design_Tools/UG949.pdf
#    - IP_Cores/PG057.pdf
#    vb.

# 3. Yeniden indexleyin
python train_rag_complete.py --reindex
```

## 💰 Maliyet

- **İlk eğitim:** ~$0.01 (6 MD dosya)
- **Her soru:** ~$0.02-0.05 (GPT-4 Turbo)
- **Aylık (100 soru):** ~$10

GPT-3.5 kullanarak %90 tasarruf edebilirsiniz (ama kalite düşer).

## 📚 Detaylı Dokümantasyon

[RAG_TRAINING_GUIDE.md](RAG_TRAINING_GUIDE.md) dosyasında her şey detaylı açıklanmış.

## ❓ Sorun mu var?

### OpenAI API Key hatası
```powershell
# .env dosyasını kontrol edin
cat .env
```

### Collection not found
```powershell
# Önce eğitim yapın
python train_rag_complete.py
```

### Paket yok hatası
```powershell
pip install -r requirements.txt
```

---

**🎉 Hepsi bu kadar! Artık Vivado uzmanı AI asistanınız hazır!**
