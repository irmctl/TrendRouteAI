"""
TrendRouteAI Test Suite
Rota önerisi ve agent fonksiyonları için testler
"""

import pytest
from datetime import date
from app.schemas import UserRequest
from app.agent.agent import (
    extract_profile_from_request,
    score_route,
    generate_suggestions,
    get_route_detail
)
from app.data.dummy_data import DUMMY_DATA

class TestProfileExtraction:
    """Profil çıkarma testleri"""
    
    def test_basic_profile_extraction(self):
        """Temel profil çıkarma testi"""
        request = UserRequest(
            intent="İstanbul'da tarihi yerler görmek istiyorum",
            budget_tl=1000,
            interests=["tarih", "kültür"],
            max_results=4
        )
        
        profile = extract_profile_from_request(request)
        
        assert profile["budget_tl"] == 1000
        assert profile["interests"] == ["tarih", "kültür"]
        assert profile["duration_days"] == 1
        assert profile["max_results"] == 4
    
    def test_date_duration_calculation(self):
        """Tarih aralığından süre hesaplama testi"""
        request = UserRequest(
            intent="Hafta sonu kaçamağı",
            start_date=date(2024, 1, 6),  # Cumartesi
            end_date=date(2024, 1, 7),    # Pazar
            max_results=4
        )
        
        profile = extract_profile_from_request(request)
        assert profile["duration_days"] == 2

class TestRouteScoring:
    """Rota puanlama testleri"""
    
    def test_budget_filter(self):
        """Bütçe filtreleme testi - düşük bütçe ile pahalı rotalar düşük puan almalı"""
        # Düşük bütçeli kullanıcı profili
        profile = {
            "budget_tl": 500,
            "interests": ["tarih"],
            "duration_days": 1
        }
        
        # Pahalı rota (1200 TL)
        expensive_route = {
            "city": "İzmir",
            "estimated_cost_tl": 1200,
            "activities": ["yemek", "kültür"],
            "budget_level": "Yüksek"
        }
        
        # Ucuz rota (400 TL)
        cheap_route = {
            "city": "İstanbul",
            "estimated_cost_tl": 400,
            "activities": ["tarih", "kültür"],
            "budget_level": "Düşük"
        }
        
        trending = [{"city": "İstanbul", "trend_score": 0.8}]
        
        expensive_score = score_route(expensive_route, profile, trending)
        cheap_score = score_route(cheap_route, profile, trending)
        
        # Pahalı rota daha düşük puan almalı
        assert expensive_score < cheap_score
        # Pahalı rota negatif bütçe puanı almalı
        assert expensive_score < 0.5  # Trend puanından düşük olmalı
    
    def test_interest_matching(self):
        """İlgi alanı eşleşme testi - eşleşen rotalar daha yüksek puan almalı"""
        profile = {
            "budget_tl": 1000,
            "interests": ["tarih", "müze"],
            "duration_days": 1
        }
        
        # İlgi alanları eşleşen rota
        matching_route = {
            "city": "İstanbul",
            "estimated_cost_tl": 800,
            "activities": ["tarih", "müze", "camii"],
            "budget_level": "Orta"
        }
        
        # İlgi alanları eşleşmeyen rota
        non_matching_route = {
            "city": "Antalya",
            "estimated_cost_tl": 600,
            "activities": ["deniz", "güneş", "plaj"],
            "budget_level": "Orta"
        }
        
        trending = [{"city": "İstanbul", "trend_score": 0.8}, {"city": "Antalya", "trend_score": 0.7}]
        
        matching_score = score_route(matching_route, profile, trending)
        non_matching_score = score_route(non_matching_route, profile, trending)
        
        # Eşleşen rota daha yüksek puan almalı
        assert matching_score > non_matching_score
    
    def test_trend_matching(self):
        """Trend eşleşme testi - trend lokasyonları daha yüksek puan almalı"""
        profile = {
            "budget_tl": 1000,
            "interests": ["tarih"],
            "duration_days": 1
        }
        
        # Trend lokasyon (İstanbul)
        trending_route = {
            "city": "İstanbul",
            "estimated_cost_tl": 800,
            "activities": ["tarih", "kültür"],
            "budget_level": "Orta"
        }
        
        # Trend olmayan lokasyon
        non_trending_route = {
            "city": "Ankara",
            "estimated_cost_tl": 600,
            "activities": ["tarih", "kültür"],
            "budget_level": "Orta"
        }
        
        trending = [{"city": "İstanbul", "trend_score": 0.9}]
        
        trending_score = score_route(trending_route, profile, trending)
        non_trending_score = score_route(non_trending_route, profile, trending)
        
        # Trend lokasyon daha yüksek puan almalı
        assert trending_score > non_trending_score

class TestRouteGeneration:
    """Rota üretimi testleri"""
    
    def test_generate_suggestions_basic(self):
        """Temel rota önerisi üretimi testi"""
        request = UserRequest(
            intent="İstanbul'da günübirlik tur",
            budget_tl=1000,
            interests=["tarih", "kültür"],
            max_results=4
        )
        
        profile, trending, suggestions = generate_suggestions(request)
        
        assert len(suggestions) <= 4
        assert all(hasattr(s, 'title') for s in suggestions)
        assert all(hasattr(s, 'steps') for s in suggestions)
        assert all(hasattr(s, 'budget_level') for s in suggestions)
        assert all(hasattr(s, 'cta') for s in suggestions)
    
    def test_generate_suggestions_with_date_range(self):
        """Tarih aralığı ile rota önerisi testi"""
        request = UserRequest(
            intent="Hafta sonu kaçamağı",
            start_date=date(2024, 1, 6),
            end_date=date(2024, 1, 7),
            budget_tl=1500,
            max_results=3
        )
        
        profile, trending, suggestions = generate_suggestions(request)
        
        assert profile["duration_days"] == 2
        assert len(suggestions) <= 3

class TestRouteDetails:
    """Rota detayları testleri"""
    
    def test_get_route_detail_existing(self):
        """Mevcut rota detayı alma testi"""
        route_detail = get_route_detail("route_museum_001")
        
        assert route_detail is not None
        assert route_detail.title == "Şehir Müzesi Turu"
        assert len(route_detail.steps) == 3
        assert route_detail.total_duration_minutes == 20
        assert route_detail.total_distance_m == 4.95
    
    def test_get_route_detail_nonexistent(self):
        """Var olmayan rota detayı testi"""
        route_detail = get_route_detail("nonexistent_route")
        
        assert route_detail is None

class TestDataIntegrity:
    """Veri bütünlüğü testleri"""
    
    def test_dummy_data_structure(self):
        """Dummy veri yapısı testi"""
        assert "trending_locations" in DUMMY_DATA
        assert "routes" in DUMMY_DATA
        
        # En az 4 rota olmalı
        assert len(DUMMY_DATA["routes"]) >= 4
        
        # Her rotada gerekli alanlar olmalı
        required_fields = ["route_id", "title", "subtitle", "steps", "budget_level"]
        for route in DUMMY_DATA["routes"]:
            for field in required_fields:
                assert field in route
    
    def test_route_steps_format(self):
        """Rota adımları format testi"""
        for route in DUMMY_DATA["routes"]:
            assert "steps" in route
            for step in route["steps"]:
                assert "icon" in step
                assert "label" in step
                assert isinstance(step["icon"], str)
                assert isinstance(step["label"], str)

if __name__ == "__main__":
    pytest.main([__file__]) 