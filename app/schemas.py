from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date

class UserRequest(BaseModel):
    """Kullanıcı rota önerisi isteği"""
    user_id: Optional[str] = None
    intent: str = Field(..., description="Kullanıcının rota isteği metni")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget_tl: Optional[int] = Field(None, ge=0, description="Bütçe (TL)")
    interests: Optional[List[str]] = []
    max_results: int = Field(4, ge=1, le=10, description="Maksimum sonuç sayısı")

class RouteStep(BaseModel):
    """Rota adımı - UI kartındaki ikon-trace için"""
    icon: str = Field(..., description="Adım ikonu (emoji veya icon name)")
    label: str = Field(..., description="Adım etiketi")

class CTAAction(BaseModel):
    """Call to Action - UI butonu için"""
    label: str = Field(..., description="Buton metni")
    action: str = Field(..., description="Eylem türü")
    route_id: Optional[str] = None
    url: Optional[str] = None

class RouteCard(BaseModel):
    """Rota kartı - UI suggest response için"""
    route_id: str
    title: str
    subtitle: str
    steps: List[RouteStep] = Field(..., description="UI kartındaki ikon-trace")
    approx_duration_text: str = Field(..., description="Yaklaşık süre metni")
    approx_duration_minutes: Optional[int] = None
    budget_level: str = Field(..., description="Bütçe seviyesi: Düşük/Orta/Yüksek")
    estimated_cost_tl: Optional[int] = None
    activities: List[str] = []
    coords: Optional[List[float]] = None
    score: Optional[float] = None
    reason: Optional[str] = None
    cta: CTAAction

class SuggestResponse(BaseModel):
    """Rota önerisi yanıtı"""
    user_id: Optional[str] = None
    suggestions: List[RouteCard]
    used_trends: Optional[List[Dict[str, Any]]] = None

class StepDetail(BaseModel):
    """Rota detayındaki adım bilgisi"""
    step_number: int
    mode: str = Field(..., description="Ulaşım modu (yürüme, otobüs, vb.)")
    instruction: str = Field(..., description="Adım talimatı")
    duration_minutes: int
    distance_m: int
    detail: Optional[str] = None
    icon: Optional[str] = None
    line_info: Optional[str] = None
    stops: Optional[int] = None

class RouteDetail(BaseModel):
    """Rota detayı - timeline için"""
    route_id: str
    title: str
    transport_type: str = Field(..., description="Ulaşım türü")
    start_point: str
    end_point: str
    total_duration_minutes: int
    total_distance_m: float
    summary: str
    steps: List[StepDetail]
    final_message: str
    polyline: Optional[str] = None

class FeedbackRequest(BaseModel):
    """Geri bildirim isteği"""
    route_id: str
    rating: int = Field(..., ge=1, le=5, description="1-5 arası rating")
    comment: Optional[str] = None
    user_id: Optional[str] = None 