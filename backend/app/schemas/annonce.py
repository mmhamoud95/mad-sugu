from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.annonce import AnnonceStatus, AnnonceCondition


class AnnonceImageResponse(BaseModel):
    id: int
    url: str
    order: int
    
    class Config:
        from_attributes = True


class AnnonceBase(BaseModel):
    title: str
    description: str
    price: float
    is_negotiable: bool = True
    condition: AnnonceCondition = AnnonceCondition.USED
    category_id: int
    location_city: Optional[str] = None
    location_district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AnnonceCreate(AnnonceBase):
    pass


class AnnonceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_negotiable: Optional[bool] = None
    condition: Optional[AnnonceCondition] = None
    category_id: Optional[int] = None
    location_city: Optional[str] = None
    location_district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[AnnonceStatus] = None


class AnnonceResponse(AnnonceBase):
    id: int
    user_id: int
    status: AnnonceStatus
    views_count: int
    favorites_count: int
    messages_count: int
    is_featured: bool
    is_urgent: bool
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    images: List[AnnonceImageResponse] = []
    
    class Config:
        from_attributes = True


class AnnonceListResponse(BaseModel):
    id: int
    title: str
    price: float
    location_city: Optional[str]
    is_featured: bool
    is_urgent: bool
    created_at: datetime
    images: List[AnnonceImageResponse] = []
    
    class Config:
        from_attributes = True
