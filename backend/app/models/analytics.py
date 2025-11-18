from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from ..core.database import Base


class AnnonceView(Base):
    """Track annonce views for analytics"""
    __tablename__ = "annonce_views"
    
    id = Column(Integer, primary_key=True, index=True)
    annonce_id = Column(Integer, ForeignKey("annonces.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for anonymous
    
    # User agent and location info
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Timestamps
    viewed_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    annonce = relationship("Annonce")
    user = relationship("User")


class DailyStats(Base):
    """Daily aggregated statistics"""
    __tablename__ = "daily_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    stat_date = Column(Date, nullable=False, unique=True, index=True)
    
    # User statistics
    new_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    
    # Annonce statistics
    new_annonces = Column(Integer, default=0)
    active_annonces = Column(Integer, default=0)
    sold_annonces = Column(Integer, default=0)
    
    # Engagement statistics
    total_messages = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_favorites = Column(Integer, default=0)
    
    # Revenue (for boosted annonces)
    boost_revenue = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
