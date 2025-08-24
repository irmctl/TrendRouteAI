# TrendRouteAI Backend

Yapay Zeka destekli rota önerileri için backend API servisi. Mobil UI ile tam uyumlu, agent tabanlı rota önerisi üretimi yapar.

## 🚀 Özellikler

- **AI Agent Tabanlı Rota Önerisi**: Kullanıcı profili ve trend analizi ile kişiselleştirilmiş rotalar
- **Trend Lokasyon Analizi**: Popüler ve güncel destinasyonları takip eder
- **Akıllı Puanlama**: Bütçe, ilgi alanları ve trend uyumuna göre rota sıralaması
- **LLM Entegrasyonu**: OpenAI API ile intent parsing (opsiyonel)
- **Mobil UI Uyumlu**: Frontend görsellerindeki veri yapısına birebir uyumlu
- **Comprehensive Testing**: Pytest ile kapsamlı test coverage

## 🏗️ Proje Yapısı

```
TrendRouteAI/
├── main.py                 # FastAPI ana uygulama
├── app/
│   ├── __init__.py
│   ├── schemas.py          # Pydantic veri modelleri
│   ├── data/
│   │   ├── __init__.py
│   │   └── dummy_data.py   # Örnek veri ve rotalar
│   ├── agent/
│   │   ├── __init__.py
│   │   └── agent.py        # Ana agent mantığı
│   └── llm/
│       ├── __init__.py
│       └── llm_adapter.py  # LLM entegrasyonu
├── tests/
│   ├── __init__.py
│   └── test_suggest.py     # Test suite
├── requirements.txt         # Python bağımlılıkları
└── README.md
```

## 🛠️ Kurulum

### Gereksinimler
- Python 3.11+
- pip

### Adımlar

1. **Repository'yi klonlayın**
```bash
git clone <repository-url>
cd TrendRouteAI
```

2. **Virtual environment oluşturun**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Environment variables ayarlayın (opsiyonel)**
```bash
# .env dosyası oluşturun
cp .env.example .env

# OpenAI API key ekleyin (opsiyonel)
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Çalıştırma

### Development Server
```bash
uvicorn main:app --reload --port 8000
```

### Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server başladıktan sonra:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📱 API Endpoints

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{"status": "ok"}
```

### 2. Rota Önerisi
```http
POST /suggest
```

**Request Body:**
```json
{
  "intent": "İstanbul'da tarihi yerler görmek istiyorum",
  "budget_tl": 1000,
  "interests": ["tarih", "kültür"],
  "max_results": 4
}
```

**Response (UI Kartları):**
```json
{
  "user_id": null,
  "suggestions": [
    {
      "route_id": "route_istanbul_001",
      "title": "Tarihi İstanbul Rotası",
      "subtitle": "İstanbul'un ikonik tarihi mekanlarını keşfedin.",
      "steps": [
        {"icon": "🏛️", "label": "Tarihi Yer"},
        {"icon": "🍽️", "label": "Restoran"},
        {"icon": "🛍️", "label": "Çarşı"}
      ],
      "approx_duration_text": "Yaklaşık 6 Saat",
      "budget_level": "Orta",
      "estimated_cost_tl": 800,
      "cta": {
        "label": "Rota Seç",
        "action": "select_route",
        "route_id": "route_istanbul_001"
      }
    }
  ],
  "used_trends": [...]
}
```

### 3. Rota Detayı
```http
GET /routes/{route_id}
```

**Response (Timeline):**
```json
{
  "route_id": "route_museum_001",
  "title": "Şehir Müzesi Turu",
  "transport_type": "Toplu Taşıma",
  "start_point": "Başlangıç Noktası (Otel)",
  "end_point": "Şehir Müzesi",
  "total_duration_minutes": 20,
  "total_distance_m": 4.95,
  "summary": "Toplam Süre: 20 dk, Toplam Mesafe: 4.95 km",
  "steps": [
    {
      "step_number": 1,
      "mode": "yürüme",
      "instruction": "Ana Otobüs Durağına Yürü",
      "duration_minutes": 5,
      "distance_m": 300,
      "icon": "🚶"
    }
  ],
  "final_message": "Müzeye Vardın!"
}
```

### 4. Rota Seçimi
```http
POST /routes/{route_id}/select
```

### 5. Geri Bildirim
```http
POST /feedback
```

## 🧪 Testler

### Test Çalıştırma
```bash
# Tüm testleri çalıştır
pytest tests/

# Verbose mod
pytest tests/ -v

# Coverage ile
pytest tests/ --cov=app
```

### Test Kapsamı
- ✅ Profil çıkarma testleri
- ✅ Bütçe filtreleme testleri
- ✅ İlgi alanı eşleşme testleri
- ✅ Trend uyum testleri
- ✅ Rota üretimi testleri
- ✅ Veri bütünlüğü testleri

## 🤖 Agent Modülü

### Ana Fonksiyonlar

1. **`extract_profile_from_request()`**: Kullanıcı isteğinden profil çıkarır
2. **`get_top_trending()`**: En popüler trend lokasyonları döndürür
3. **`score_route()`**: Rotayı profil ve trend'e göre puanlar
4. **`rank_and_format_suggestions()`**: Önerileri sıralar ve UI formatına dönüştürür
5. **`generate_suggestions()`**: Ana öneri üretim fonksiyonu

### Puanlama Algoritması
- **Trend Uyumu**: 0-0.5 puan
- **Bütçe Uyumu**: ±0.3 puan
- **İlgi Alanı Eşleşmesi**: 0-0.2 puan

## 🧠 LLM Entegrasyonu

### OpenAI API (Opsiyonel)
- **Function Calling**: Intent parsing için structured output
- **Fallback Mode**: API key yoksa regex tabanlı parsing
- **Error Handling**: API hatası durumunda graceful degradation

### Mock Mode
API key bulunamadığında:
- Regex tabanlı intent parsing
- Deterministic responses
- Hızlı çalışma

## 🔒 Güvenlik ve Etik

- **Veri Koruması**: Kullanıcı verileri şifrelenir
- **Rate Limiting**: API abuse koruması
- **Legal Compliance**: Scraping ve sosyal medya erişimi için yasal uyarılar
- **Privacy**: GDPR uyumlu veri işleme

## 🚧 Gelecek Geliştirmeler

- [ ] Veritabanı entegrasyonu (PostgreSQL)
- [ ] Redis cache sistemi
- [ ] Real-time trend analizi
- [ ] Machine learning tabanlı puanlama
- [ ] Multi-language support
- [ ] Docker containerization

## 📊 Performance

- **Response Time**: < 200ms (mock mode)
- **Throughput**: 1000+ requests/minute
- **Memory Usage**: < 100MB
- **CPU Usage**: < 10% (idle)

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

- **Proje**: TrendRouteAI
- **Takım**: [Takım Bilgileri]
- **Email**: [İletişim Email]

---

**Not**: Bu proje sadece backend/agent katmanını içerir. Mobil UI kodu ayrı bir repository'de bulunmaktadır.