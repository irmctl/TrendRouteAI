"""
TrendRouteAI Dummy Data
UI görsellerindeki rotalara uygun örnek veriler
"""

DUMMY_DATA = {
    "trending_locations": [
        {
            "city": "Kapadokya",
            "popularity": 95,
            "reason": "Balon turları trend",
            "coords": [38.6431, 34.8283],
            "trend_score": 0.95
        },
        {
            "city": "İstanbul",
            "popularity": 88,
            "reason": "Tarihi mekanlar ve Boğaz turu",
            "coords": [41.0082, 28.9784],
            "trend_score": 0.88
        },
        {
            "city": "Antalya",
            "popularity": 82,
            "reason": "Sahil ve doğa aktiviteleri",
            "coords": [36.8969, 30.7133],
            "trend_score": 0.82
        },
        {
            "city": "İzmir",
            "popularity": 75,
            "reason": "Ege mutfağı ve kültür",
            "coords": [38.4192, 27.1287],
            "trend_score": 0.75
        }
    ],
    "routes": [
        {
            "route_id": "route_istanbul_001",
            "route_name": "Tarihi İstanbul Rotası",
            "title": "Tarihi İstanbul Rotası",
            "subtitle": "İstanbul'un ikonik tarihi mekanlarını keşfedin.",
            "city": "İstanbul",
            "estimated_cost_tl": 800,
            "activities": ["tarih", "kültür", "müze", "camii"],
            "duration_days": 1,
            "approx_duration_minutes": 360,
            "budget_level": "Orta",
            "coords": [41.0082, 28.9784],
            "steps": [
                {"icon": "🏛️", "label": "Tarihi Yer"},
                {"icon": "🍽️", "label": "Restoran"},
                {"icon": "🛍️", "label": "Çarşı"}
            ],
            "detail_steps": [
                {
                    "step_number": 1,
                    "mode": "yürüme",
                    "instruction": "Sultanahmet Meydanına Yürü",
                    "duration_minutes": 10,
                    "distance_m": 500,
                    "icon": "🚶"
                },
                {
                    "step_number": 2,
                    "mode": "yürüme",
                    "instruction": "Ayasofya'yı Ziyaret Et",
                    "duration_minutes": 90,
                    "distance_m": 0,
                    "icon": "🏛️"
                },
                {
                    "step_number": 3,
                    "mode": "yürüme",
                    "instruction": "Topkapı Sarayına Git",
                    "duration_minutes": 120,
                    "distance_m": 800,
                    "icon": "🏰"
                }
            ]
        },
        {
            "route_id": "route_bosphorus_001",
            "route_name": "Boğaz Hattı Turu",
            "title": "Boğaz Hattı Turu",
            "subtitle": "Boğazın eşsiz manzarasında huzurlu bir gün.",
            "city": "İstanbul",
            "estimated_cost_tl": 400,
            "activities": ["manzara", "doğa", "huzur", "fotoğraf"],
            "duration_days": 1,
            "approx_duration_minutes": 240,
            "budget_level": "Düşük",
            "coords": [41.0082, 28.9784],
            "steps": [
                {"icon": "☕", "label": "Kafe"},
                {"icon": "🌳", "label": "Park"},
                {"icon": "📸", "label": "Manzara"}
            ],
            "detail_steps": [
                {
                    "step_number": 1,
                    "mode": "metro",
                    "instruction": "Taksim Metroya Bin",
                    "duration_minutes": 15,
                    "distance_m": 2000,
                    "icon": "🚇"
                },
                {
                    "step_number": 2,
                    "mode": "yürüme",
                    "instruction": "Gülhane Parkına Git",
                    "duration_minutes": 20,
                    "distance_m": 1000,
                    "icon": "🌳"
                }
            ]
        },
        {
            "route_id": "route_anatolia_001",
            "route_name": "Anadolu Lezzetleri",
            "title": "Anadolu Lezzetleri",
            "subtitle": "Yöresel tatlar ve geleneksel dükkanlar.",
            "city": "İzmir",
            "estimated_cost_tl": 1200,
            "activities": ["yemek", "alışveriş", "el sanatı", "kültür"],
            "duration_days": 1,
            "approx_duration_minutes": 300,
            "budget_level": "Yüksek",
            "coords": [38.4192, 27.1287],
            "steps": [
                {"icon": "🍽️", "label": "Yöresel"},
                {"icon": "🛍️", "label": "Dükkan"},
                {"icon": "🎨", "label": "El Sanatı"}
            ],
            "detail_steps": [
                {
                    "step_number": 1,
                    "mode": "yürüme",
                    "instruction": "Kemeraltı Çarşısına Git",
                    "duration_minutes": 25,
                    "distance_m": 1500,
                    "icon": "🛍️"
                },
                {
                    "step_number": 2,
                    "mode": "yürüme",
                    "instruction": "Yöresel Restoranlarda Yemek Ye",
                    "duration_minutes": 90,
                    "distance_m": 0,
                    "icon": "🍽️"
                }
            ]
        },
        {
            "route_id": "route_islands_001",
            "route_name": "Adalar Kaçamağı",
            "title": "Adalar Kaçamağı",
            "subtitle": "Şehrin gürültüsünden uzak, sakin bir ada gezisi.",
            "city": "İstanbul",
            "estimated_cost_tl": 600,
            "activities": ["doğa", "deniz", "huzur", "yemek"],
            "duration_days": 1,
            "approx_duration_minutes": 420,
            "budget_level": "Orta",
            "coords": [40.8761, 29.0897],
            "steps": [
                {"icon": "⛴️", "label": "Feribot"},
                {"icon": "🌳", "label": "Doğa"},
                {"icon": "🐟", "label": "Deniz Ürünü"}
            ],
            "detail_steps": [
                {
                    "step_number": 1,
                    "mode": "feribot",
                    "instruction": "Kadıköy'den Büyükada'ya Feribotla Git",
                    "duration_minutes": 90,
                    "distance_m": 15000,
                    "icon": "⛴️"
                },
                {
                    "step_number": 2,
                    "mode": "yürüme",
                    "instruction": "Ada Etrafında Yürüyüş Yap",
                    "duration_minutes": 180,
                    "distance_m": 8000,
                    "icon": "🚶"
                }
            ]
        }
    ]
}

# Rota detayları için ayrı veri
DUMMY_ROUTE_DETAILS = {
    "route_museum_001": {
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
                "icon": "🚶",
                "detail": "Otelden çıkıp ana caddeye yönel"
            },
            {
                "step_number": 2,
                "mode": "otobüs",
                "instruction": "29B Nolu Otobüse Bin - 5 Durak",
                "duration_minutes": 12,
                "distance_m": 4500,
                "icon": "🚌",
                "line_info": "29B",
                "stops": 5
            },
            {
                "step_number": 3,
                "mode": "yürüme",
                "instruction": "Müze Girişine Yürü",
                "duration_minutes": 3,
                "distance_m": 150,
                "icon": "🚶",
                "detail": "Otobüsten inip müze binasına yönel"
            }
        ],
        "final_message": "Müzeye Vardın!",
        "polyline": None
    }
}

# UI kartları için CTA verileri
CTA_TEMPLATES = {
    "select_route": {
        "label": "Rota Seç",
        "action": "select_route"
    },
    "view_details": {
        "label": "Detayları Gör",
        "action": "view_details"
    }
} 