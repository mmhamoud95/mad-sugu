from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class NotificationType(enum.Enum):
    """Types of notifications"""
    NEW_MESSAGE = "new_message"
    NEW_FAVORITE = "new_favorite"
    ANNONCE_SOLD = "annonce_sold"
    ANNONCE_EXPIRED = "annonce_expired"
    ALERT_MATCHED = "alert_matched"
    NEW_REVIEW = "new_review"
    BOOST_EXPIRED = "boost_expired"
    ADMIN_MESSAGE = "admin_message"


class Notification(Base):
    """Notification model for push and in-app notifications"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Notification content
    type = Column(Enum(NotificationType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Related entities
    annonce_id = Column(Integer, ForeignKey("annonces.id"), nullable=True)
    related_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # e.g., who sent message
    
    # Status
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    
    # Push notification
    is_push_sent = Column(Boolean, default=False)
    push_sent_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="notifications")
    annonce = relationship("Annonce", backref="notifications")
    related_user = relationship("User", foreign_keys=[related_user_id])
