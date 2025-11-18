from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class AnnonceViewCreate(BaseModel):
    annonce_id: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class DailyStatsResponse(BaseModel):
    stat_date: date
    new_users: int
    active_users: int
    new_annonces: int
    active_annonces: int
    sold_annonces: int
    total_messages: int
    total_views: int
    total_favorites: int
    boost_revenue: float
    
    class Config:
        from_attributes = True


class AnalyticsSummary(BaseModel):
    """Summary analytics for dashboard"""
    total_users: int
    total_annonces: int
    active_annonces: int
    total_messages: int
    total_views: int
    total_favorites: int
    total_revenue: float
    
    # Period comparison
    period_new_users: int
    period_new_annonces: int
    period_views: int
    period_messages: int


class UserAnalytics(BaseModel):
    """Analytics for a specific user"""
    user_id: int
    total_annonces: int
    active_annonces: int
    sold_annonces: int
    total_views: int
    total_messages_received: int
    total_favorites_received: int
    average_rating: float
    total_reviews: int
