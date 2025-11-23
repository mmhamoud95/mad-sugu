from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Review(Base):
    """Review model for rating users and their annonces"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    
    # Foreign Keys
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who gave the review
    reviewed_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who received the review
    annonce_id = Column(Integer, ForeignKey("annonces.id"), nullable=True)  # Optional: related annonce
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviewer = relationship("User", foreign_keys=[reviewer_id], backref="reviews_given")
    reviewed_user = relationship("User", foreign_keys=[reviewed_user_id], backref="reviews_received")
    annonce = relationship("Annonce", backref="reviews")
