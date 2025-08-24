"""
TrendRouteAI Agent Module
Rota önerisi üretimi ve yönetimi için ana mantık
"""

from typing import List, Dict, Tuple, Optional
from datetime import date
import logging
from app.schemas import UserRequest, RouteCard, RouteDetail, RouteStep, CTAAction
from app.data.dummy_data import DUMMY_DATA, DUMMY_ROUTE_DETAILS, CTA_TEMPLATES

logger = logging.getLogger(__name__)

def extract_profile_from_request(req: UserRequest) -> dict:
    """
    Kullanıcı isteğinden profil bilgilerini çıkarır
    
    Args:
        req: Kullanıcı isteği
        
    Returns:
        Profil sözlüğü
    """
    profile = {
        "budget_tl": req.budget_tl,
        "interests": req.interests or [],
        "duration_days": 1,
        "max_results": req.max_results
    }
    
    # Tarih aralığından süre hesapla
    if req.start_date and req.end_date:
        delta = req.end_date - req.start_date
        profile["duration_days"] = delta.days + 1
    
    return profile

def get_top_trending(n: int = 4) -> List[dict]:
    """
    En popüler trend lokasyonları döndürür
    
    Args:
        n: Döndürülecek lokasyon sayısı
        
    Returns:
        Trend lokasyon listesi
    """
    trending = DUMMY_DATA.get("trending_locations", [])
    # Popülerliğe göre sırala
    sorted_trending = sorted(trending, key=lambda x: x.get("popularity", 0), reverse=True)
    return sorted_trending[:n]

def score_route(route: dict, profile: dict, trending: List[dict]) -> float:
    """
    Rotayı profil ve trend bilgilerine göre puanlar
    
    Args:
        route: Rota verisi
        profile: Kullanıcı profili
        trending: Trend lokasyonlar
        
    Returns:
        Puan (0.0 - 1.0)
    """
    score = 0.0
    
    # 1. Trend uyumu (0-0.5)
    trend_score = 0.0
    route_city = route.get("city", "")
    for trend in trending:
        if trend.get("city") == route_city:
            trend_score = trend.get("trend_score", 0.0) * 0.5
            break
    score += trend_score
    
    # 2. Bütçe uyumu (±0.3)
    budget_score = 0.0
    if profile.get("budget_tl") and route.get("estimated_cost_tl"):
        user_budget = profile["budget_tl"]
        route_cost = route["estimated_cost_tl"]
        
        if user_budget >= route_cost:
            # Bütçe yeterli - pozitif puan
            budget_score = 0.3 * (1 - (route_cost / user_budget))
        else:
            # Bütçe yetersiz - negatif puan
            budget_score = -0.3 * ((route_cost - user_budget) / route_cost)
    
    score += budget_score
    
    # 3. İlgi alanı eşleşmesi (0-0.2)
    interest_score = 0.0
    user_interests = profile.get("interests", [])
    route_activities = route.get("activities", [])
    
    if user_interests and route_activities:
        matches = sum(1 for interest in user_interests if interest in route_activities)
        if matches > 0:
            interest_score = 0.2 * (matches / len(user_interests))
    
    score += interest_score
    
    # Puanı 0-1 arasında sınırla
    return max(0.0, min(1.0, score))

def rank_and_format_suggestions(
    candidates: List[dict], 
    profile: dict, 
    trending: List[dict], 
    max_results: int
) -> List[RouteCard]:
    """
    Aday rotaları puanla, sırala ve UI formatına dönüştür
    
    Args:
        candidates: Aday rota listesi
        profile: Kullanıcı profili
        trending: Trend lokasyonlar
        max_results: Maksimum sonuç sayısı
        
    Returns:
        Formatlanmış rota kartları
    """
    # Her rotayı puanla
    scored_routes = []
    for route in candidates:
        score = score_route(route, profile, trending)
        scored_routes.append((route, score))
    
    # Puana göre sırala (yüksekten düşüğe)
    scored_routes.sort(key=lambda x: x[1], reverse=True)
    
    # En iyi sonuçları al
    top_routes = scored_routes[:max_results]
    
    # UI formatına dönüştür
    route_cards = []
    for route, score in top_routes:
        # Süre metnini oluştur
        duration_minutes = route.get("approx_duration_minutes", 0)
        if duration_minutes >= 60:
            hours = duration_minutes // 60
            duration_text = f"Yaklaşık {hours} Saat"
        else:
            duration_text = f"Yaklaşık {duration_minutes} Dakika"
        
        # CTA oluştur
        cta = CTAAction(
            label="Rota Seç",
            action="select_route",
            route_id=route["route_id"]
        )
        
        # RouteStep listesi oluştur
        steps = []
        for step_data in route.get("steps", []):
            step = RouteStep(
                icon=step_data["icon"],
                label=step_data["label"]
            )
            steps.append(step)
        
        # RouteCard oluştur
        route_card = RouteCard(
            route_id=route["route_id"],
            title=route["title"],
            subtitle=route["subtitle"],
            steps=steps,
            approx_duration_text=duration_text,
            approx_duration_minutes=duration_minutes,
            budget_level=route["budget_level"],
            estimated_cost_tl=route.get("estimated_cost_tl"),
            activities=route.get("activities", []),
            coords=route.get("coords"),
            score=score,
            reason=f"Trend: {route.get('city', 'Bilinmeyen')}, Bütçe: {route['budget_level']}",
            cta=cta
        )
        
        route_cards.append(route_card)
    
    return route_cards

def generate_suggestions(req: UserRequest) -> Tuple[dict, List[dict], List[RouteCard]]:
    """
    Ana öneri üretim fonksiyonu
    
    Args:
        req: Kullanıcı isteği
        
    Returns:
        (profil, kullanılan_trendler, öneriler) tuple'ı
    """
    try:
        # 1. Profil çıkar
        profile = extract_profile_from_request(req)
        logger.info(f"Kullanıcı profili çıkarıldı: {profile}")
        
        # 2. Trend lokasyonları al
        trending = get_top_trending(4)
        logger.info(f"Trend lokasyonlar alındı: {len(trending)} adet")
        
        # 3. Tüm rotaları al (gerçek uygulamada filtreleme yapılabilir)
        all_routes = DUMMY_DATA.get("routes", [])
        
        # 4. Önerileri üret ve formatla
        suggestions = rank_and_format_suggestions(
            all_routes, profile, trending, req.max_results
        )
        
        logger.info(f"{len(suggestions)} adet rota önerisi üretildi")
        
        return profile, trending, suggestions
        
    except Exception as e:
        logger.error(f"Öneri üretiminde hata: {str(e)}")
        raise

def get_route_detail(route_id: str) -> Optional[RouteDetail]:
    """
    Belirli bir rotanın detaylarını döndürür
    
    Args:
        route_id: Rota ID'si
        
    Returns:
        Rota detayı veya None
    """
    try:
        route_data = DUMMY_ROUTE_DETAILS.get(route_id)
        if not route_data:
            return None
        
        # StepDetail listesi oluştur
        steps = []
        for step_data in route_data["steps"]:
            step = {
                "step_number": step_data["step_number"],
                "mode": step_data["mode"],
                "instruction": step_data["instruction"],
                "duration_minutes": step_data["duration_minutes"],
                "distance_m": step_data["distance_m"],
                "detail": step_data.get("detail"),
                "icon": step_data.get("icon"),
                "line_info": step_data.get("line_info"),
                "stops": step_data.get("stops")
            }
            steps.append(step)
        
        # RouteDetail oluştur
        route_detail = RouteDetail(
            route_id=route_data["route_id"],
            title=route_data["title"],
            transport_type=route_data["transport_type"],
            start_point=route_data["start_point"],
            end_point=route_data["end_point"],
            total_duration_minutes=route_data["total_duration_minutes"],
            total_distance_m=route_data["total_distance_m"],
            summary=route_data["summary"],
            steps=steps,
            final_message=route_data["final_message"],
            polyline=route_data.get("polyline")
        )
        
        return route_detail
        
    except Exception as e:
        logger.error(f"Rota detayı alınırken hata: {str(e)}")
        return None

def select_route(route_id: str, user_id: Optional[str]) -> dict:
    """
    Rota seçimi kaydeder (analytics mock)
    
    Args:
        route_id: Seçilen rota ID'si
        user_id: Kullanıcı ID'si
        
    Returns:
        Kayıt sonucu
    """
    try:
        # Gerçek uygulamada veritabanına kaydedilir
        logger.info(f"Rota seçimi kaydedildi: {route_id}, Kullanıcı: {user_id}")
        
        return {
            "status": "success",
            "route_id": route_id,
            "user_id": user_id,
            "timestamp": "2024-01-01T12:00:00Z",
            "message": "Rota seçimi başarıyla kaydedildi"
        }
        
    except Exception as e:
        logger.error(f"Rota seçimi kaydedilirken hata: {str(e)}")
        return {
            "status": "error",
            "message": "Rota seçimi kaydedilemedi"
        }

def log_feedback(
    route_id: str, 
    user_id: Optional[str], 
    rating: int, 
    comment: Optional[str]
) -> dict:
    """
    Kullanıcı geri bildirimini kaydeder
    
    Args:
        route_id: Rota ID'si
        user_id: Kullanıcı ID'si
        rating: 1-5 arası rating
        comment: Opsiyonel yorum
        
    Returns:
        Kayıt sonucu
    """
    try:
        # Gerçek uygulamada veritabanına kaydedilir
        logger.info(f"Geri bildirim kaydedildi: Rota {route_id}, Rating: {rating}, Kullanıcı: {user_id}")
        
        if comment:
            logger.info(f"Yorum: {comment}")
        
        return {
            "status": "success",
            "route_id": route_id,
            "user_id": user_id,
            "rating": rating,
            "comment": comment,
            "timestamp": "2024-01-01T12:00:00Z",
            "message": "Geri bildirim başarıyla kaydedildi"
        }
        
    except Exception as e:
        logger.error(f"Geri bildirim kaydedilirken hata: {str(e)}")
        return {
            "status": "error",
            "message": "Geri bildirim kaydedilemedi"
        } 