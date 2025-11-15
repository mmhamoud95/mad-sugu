from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
from ..core.database import Base


class AnnonceStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SOLD = "sold"
    EXPIRED = "expired"
    DISABLED = "disabled"


class AnnonceCondition(enum.Enum):
    NEW = "new"
    USED = "used"
    REFURBISHED = "refurbished"


class Annonce(Base):
    __tablename__ = "annonces"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    is_negotiable = Column(Boolean, default=True)
    condition = Column(Enum(AnnonceCondition), default=AnnonceCondition.USED)
    status = Column(Enum(AnnonceStatus), default=AnnonceStatus.DRAFT, index=True)
    
    # Foreign Keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Location
    location_city = Column(String(100), index=True)
    location_district = Column(String(100))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Statistics
    views_count = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)
    messages_count = Column(Integer, default=0)
    
    # Featured/Premium
    is_featured = Column(Boolean, default=False)
    featured_until = Column(DateTime, nullable=True)
    is_urgent = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    
    # Relationships
    user = relationship("User", back_populates="annonces")
    category = relationship("Category", back_populates="annonces")
    images = relationship("AnnonceImage", back_populates="annonce", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="annonce", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="annonce", cascade="all, delete-orphan")


class AnnonceImage(Base):
    __tablename__ = "annonce_images"
    
    id = Column(Integer, primary_key=True, index=True)
    annonce_id = Column(Integer, ForeignKey("annonces.id"), nullable=False)
    url = Column(String, nullable=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    annonce = relationship("Annonce", back_populates="images")
