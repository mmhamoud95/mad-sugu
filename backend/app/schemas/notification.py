from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class NotificationType(str, Enum):
    """Types of notifications"""
    NEW_MESSAGE = "new_message"
    NEW_FAVORITE = "new_favorite"
    ANNONCE_SOLD = "annonce_sold"
    ANNONCE_EXPIRED = "annonce_expired"
    ALERT_MATCHED = "alert_matched"
    NEW_REVIEW = "new_review"
    BOOST_EXPIRED = "boost_expired"
    ADMIN_MESSAGE = "admin_message"


class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    message: str
    annonce_id: Optional[int] = None
    related_user_id: Optional[int] = None


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationInDB(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    read_at: Optional[datetime] = None
    is_push_sent: bool
    push_sent_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class Notification(NotificationInDB):
    pass
