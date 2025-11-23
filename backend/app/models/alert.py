from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Alert(Base):
    """Alert model for personalized notifications about new annonces"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Alert criteria
    title = Column(String(100), nullable=False)  # User-friendly name for the alert
    keywords = Column(String(500), nullable=True)  # Search keywords
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    location_city = Column(String(100), nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    
    # Settings
    is_active = Column(Boolean, default=True)
    frequency = Column(String(20), default="instant")  # instant, daily, weekly
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_triggered = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", backref="alerts")
    category = relationship("Category", backref="alerts")
