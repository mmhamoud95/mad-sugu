from pydantic import BaseModel
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int
    order: int
    subcategories: List["CategoryResponse"] = []
    
    class Config:
        from_attributes = True


# Update forward reference
CategoryResponse.model_rebuild()
