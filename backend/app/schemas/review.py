from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating from 1 to 5 stars")
    comment: Optional[str] = Field(None, max_length=1000)
    annonce_id: Optional[int] = None


class ReviewCreate(ReviewBase):
    reviewed_user_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    comment: Optional[str] = Field(None, max_length=1000)


class ReviewInDB(ReviewBase):
    id: int
    reviewer_id: int
    reviewed_user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Review(ReviewInDB):
    pass


class ReviewWithUser(Review):
    """Review with reviewer information"""
    reviewer_name: Optional[str] = None
    reviewer_email: Optional[str] = None
