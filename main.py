from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import UserRequest, SuggestResponse, RouteDetail
from app.agent.agent import generate_suggestions, get_route_detail, select_route, log_feedback
from app.data.dummy_data import DUMMY_DATA
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TrendRouteAI API",
    description="Yapay Zeka destekli rota önerileri API'si",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {"status": "ok"}

@app.get("/dummy-data")
async def get_dummy_data():
    """Dummy veri endpoint'i - geliştirme amaçlı"""
    return DUMMY_DATA

@app.post("/suggest", response_model=SuggestResponse)
async def suggest_routes(request: UserRequest):
    """
    Kullanıcı isteğine göre rota önerileri üretir
    """
    try:
        profile, used_trends, suggestions = generate_suggestions(request)
        
        return SuggestResponse(
            user_id=request.user_id,
            suggestions=suggestions,
            used_trends=used_trends
        )
    except Exception as e:
        logger.error(f"Rota önerisi üretilirken hata: {str(e)}")
        raise HTTPException(status_code=500, detail="Rota önerisi üretilemedi")

@app.get("/routes/{route_id}", response_model=RouteDetail)
async def get_route_details(route_id: str):
    """
    Belirli bir rotanın detaylarını döndürür
    """
    try:
        route_detail = get_route_detail(route_id)
        if not route_detail:
            raise HTTPException(status_code=404, detail="Rota bulunamadı")
        return route_detail
    except Exception as e:
        logger.error(f"Rota detayı alınırken hata: {str(e)}")
        raise HTTPException(status_code=500, detail="Rota detayı alınamadı")

@app.post("/routes/{route_id}/select")
async def select_route_endpoint(route_id: str, user_id: str = None):
    """
    Rota seçimi bildirimi - analytics amaçlı
    """
    try:
        result = select_route(route_id, user_id)
        return {"message": "Rota seçimi kaydedildi", "route_id": route_id, "result": result}
    except Exception as e:
        logger.error(f"Rota seçimi kaydedilirken hata: {str(e)}")
        raise HTTPException(status_code=500, detail="Rota seçimi kaydedilemedi")

@app.post("/feedback")
async def submit_feedback(route_id: str, rating: int, comment: str = None, user_id: str = None):
    """
    Kullanıcı geri bildirimi kaydeder
    """
    try:
        if not 1 <= rating <= 5:
            raise HTTPException(status_code=400, detail="Rating 1-5 arasında olmalı")
        
        result = log_feedback(route_id, user_id, rating, comment)
        return {"message": "Geri bildirim kaydedildi", "result": result}
    except Exception as e:
        logger.error(f"Geri bildirim kaydedilirken hata: {str(e)}")
        raise HTTPException(status_code=500, detail="Geri bildirim kaydedilemedi")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 