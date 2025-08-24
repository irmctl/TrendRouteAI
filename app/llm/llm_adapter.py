"""
TrendRouteAI LLM Adapter
OpenAI entegrasyonu ve fallback mock fonksiyonları
"""

import os
import re
import logging
from typing import Dict, List, Optional
import time

logger = logging.getLogger(__name__)

# OpenAI API key kontrolü
OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))

def parse_intent_with_llm(text: str) -> dict:
    """
    Kullanıcı intent metnini LLM ile parse eder
    
    Args:
        text: Kullanıcı metni
        
    Returns:
        Parse edilmiş intent bilgileri
    """
    if not OPENAI_AVAILABLE:
        return _mock_intent_parsing(text)
    
    try:
        # OpenAI function calling örneği (gerçek implementasyon)
        return _openai_intent_parsing(text)
    except Exception as e:
        logger.warning(f"OpenAI çağrısı başarısız, mock kullanılıyor: {str(e)}")
        return _mock_intent_parsing(text)

def refine_suggestions_with_llm(profile: dict, candidates: List[dict]) -> List[dict]:
    """
    Rota önerilerini LLM ile zenginleştirir
    
    Args:
        profile: Kullanıcı profili
        candidates: Aday rotalar
        
    Returns:
        Zenginleştirilmiş rotalar
    """
    if not OPENAI_AVAILABLE:
        return candidates  # Identity passthrough
    
    try:
        return _openai_refine_suggestions(profile, candidates)
    except Exception as e:
        logger.warning(f"OpenAI zenginleştirme başarısız, orijinal veri döndürülüyor: {str(e)}")
        return candidates

def _mock_intent_parsing(text: str) -> dict:
    """
    Mock intent parsing - regex tabanlı fallback
    """
    result = {
        "intent": "genel_gezi",
        "budget_level": "orta",
        "duration_preference": "günübirlik",
        "interests": [],
        "location_preference": None
    }
    
    text_lower = text.lower()
    
    # Bütçe seviyesi tespiti
    if any(word in text_lower for word in ["ucuz", "düşük", "ekonomik", "bütçe dostu"]):
        result["budget_level"] = "düşük"
    elif any(word in text_lower for word in ["pahalı", "lüks", "yüksek", "premium"]):
        result["budget_level"] = "yüksek"
    
    # Süre tercihi
    if any(word in text_lower for word in ["günübirlik", "1 gün", "kısa"]):
        result["duration_preference"] = "günübirlik"
    elif any(word in text_lower for word in ["hafta sonu", "2 gün", "uzun"]):
        result["duration_preference"] = "hafta_sonu"
    elif any(word in text_lower for word in ["tatil", "1 hafta", "uzun"]):
        result["duration_preference"] = "tatil"
    
    # İlgi alanları
    interests = []
    if any(word in text_lower for word in ["tarih", "müze", "saray", "camii"]):
        interests.append("tarih")
    if any(word in text_lower for word in ["doğa", "park", "orman", "deniz"]):
        interests.append("doğa")
    if any(word in text_lower for word in ["yemek", "restoran", "kafe", "lezzet"]):
        interests.append("yemek")
    if any(word in text_lower for word in ["alışveriş", "çarşı", "mağaza", "souvenir"]):
        interests.append("alışveriş")
    
    result["interests"] = interests
    
    # Lokasyon tercihi
    if "istanbul" in text_lower:
        result["location_preference"] = "İstanbul"
    elif "kapadokya" in text_lower:
        result["location_preference"] = "Kapadokya"
    elif "antalya" in text_lower:
        result["location_preference"] = "Antalya"
    elif "izmir" in text_lower:
        result["location_preference"] = "İzmir"
    
    return result

def _openai_intent_parsing(text: str) -> dict:
    """
    OpenAI ile intent parsing (function calling örneği)
    """
    # Bu fonksiyon sadece OPENAI_API_KEY varsa çalışır
    # Gerçek implementasyon için OpenAI client kullanılır
    
    # Function calling şeması örneği:
    functions = [
        {
            "name": "extract_travel_intent",
            "description": "Kullanıcının seyahat isteğinden intent bilgilerini çıkar",
            "parameters": {
                "type": "object",
                "properties": {
                    "intent": {
                        "type": "string",
                        "enum": ["genel_gezi", "tarih_turu", "doğa_turu", "yemek_turu", "alışveriş_turu"]
                    },
                    "budget_level": {
                        "type": "string",
                        "enum": ["düşük", "orta", "yüksek"]
                    },
                    "duration_preference": {
                        "type": "string",
                        "enum": ["günübirlik", "hafta_sonu", "tatil"]
                    },
                    "interests": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "İlgi alanları listesi"
                    },
                    "location_preference": {
                        "type": "string",
                        "description": "Tercih edilen şehir/lokasyon"
                    }
                },
                "required": ["intent", "budget_level", "duration_preference"]
            }
        }
    ]
    
    # Mock response (gerçek implementasyonda OpenAI API çağrısı yapılır)
    logger.info("OpenAI function calling kullanılıyor (mock)")
    time.sleep(0.1)  # API çağrısı simülasyonu
    
    return {
        "intent": "genel_gezi",
        "budget_level": "orta",
        "duration_preference": "günübirlik",
        "interests": ["tarih", "kültür"],
        "location_preference": "İstanbul"
    }

def _openai_refine_suggestions(profile: dict, candidates: List[dict]) -> List[dict]:
    """
    OpenAI ile rota önerilerini zenginleştirir
    """
    # Bu fonksiyon sadece OPENAI_API_KEY varsa çalışır
    logger.info("OpenAI ile rota zenginleştirme yapılıyor (mock)")
    
    # Gerçek implementasyonda OpenAI API ile rotalar zenginleştirilir
    # Şimdilik orijinal veriyi döndür
    return candidates

def get_llm_status() -> dict:
    """
    LLM servis durumunu döndürür
    """
    return {
        "openai_available": OPENAI_AVAILABLE,
        "fallback_mode": not OPENAI_AVAILABLE,
        "message": "OpenAI API key bulunamadı, mock mod kullanılıyor" if not OPENAI_AVAILABLE else "OpenAI API aktif"
    } 