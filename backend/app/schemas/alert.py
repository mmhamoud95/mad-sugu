from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AlertBase(BaseModel):
    title: str = Field(..., max_length=100, description="User-friendly name for the alert")
    keywords: Optional[str] = Field(None, max_length=500, description="Search keywords")
    category_id: Optional[int] = None
    location_city: Optional[str] = Field(None, max_length=100)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    frequency: str = Field(default="instant", pattern="^(instant|daily|weekly)$")


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    keywords: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None
    location_city: Optional[str] = Field(None, max_length=100)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None
    frequency: Optional[str] = Field(None, pattern="^(instant|daily|weekly)$")


class AlertInDB(AlertBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_triggered: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Alert(AlertInDB):
    pass
