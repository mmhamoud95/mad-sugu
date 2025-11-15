from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from ...core.database import get_db
from ...api.deps import get_current_active_user
from ...models import Annonce, AnnonceImage, User, AnnonceStatus
from ...schemas import AnnonceCreate, AnnonceUpdate, AnnonceResponse, AnnonceListResponse
from ...services.upload import upload_service

router = APIRouter(prefix="/annonces", tags=["annonces"])


@router.get("/", response_model=List[AnnonceListResponse])
def list_annonces(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    city: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    status: Optional[AnnonceStatus] = AnnonceStatus.ACTIVE,
    db: Session = Depends(get_db)
):
    """List annonces with filters"""
    query = db.query(Annonce)
    
    # Filter by status
    if status:
        query = query.filter(Annonce.status == status)
    
    # Filter by category
    if category_id:
        query = query.filter(Annonce.category_id == category_id)
    
    # Filter by city
    if city:
        query = query.filter(Annonce.location_city.ilike(f"%{city}%"))
    
    # Search in title and description
    if search:
        query = query.filter(
            or_(
                Annonce.title.ilike(f"%{search}%"),
                Annonce.description.ilike(f"%{search}%")
            )
        )
    
    # Price range
    if min_price is not None:
        query = query.filter(Annonce.price >= min_price)
    if max_price is not None:
        query = query.filter(Annonce.price <= max_price)
    
    # Order by featured first, then by creation date
    query = query.order_by(Annonce.is_featured.desc(), Annonce.created_at.desc())
    
    # Pagination
    annonces = query.offset(skip).limit(limit).all()
    
    return annonces


@router.get("/{annonce_id}", response_model=AnnonceResponse)
def get_annonce(annonce_id: int, db: Session = Depends(get_db)):
    """Get annonce by ID"""
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    # Increment views count
    annonce.views_count += 1
    db.commit()
    
    return annonce


@router.post("/", response_model=AnnonceResponse, status_code=status.HTTP_201_CREATED)
async def create_annonce(
    annonce_data: AnnonceCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new annonce"""
    # Create annonce
    annonce = Annonce(
        **annonce_data.dict(),
        user_id=current_user.id,
        status=AnnonceStatus.DRAFT
    )
    db.add(annonce)
    db.commit()
    db.refresh(annonce)
    
    return annonce


@router.post("/{annonce_id}/images", response_model=AnnonceResponse)
async def upload_annonce_images(
    annonce_id: int,
    images: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload images for an annonce"""
    # Get annonce
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    # Check ownership
    if annonce.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this annonce"
        )
    
    # Validate number of images
    existing_images = len(annonce.images)
    if existing_images + len(images) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum 10 images allowed. You have {existing_images}, trying to add {len(images)}"
        )
    
    # Upload images
    for idx, image in enumerate(images):
        try:
            image_url = await upload_service.save_image(image, f"annonces/{annonce_id}")
            db_image = AnnonceImage(
                annonce_id=annonce.id,
                url=image_url,
                order=existing_images + idx
            )
            db.add(db_image)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload image: {str(e)}"
            )
    
    db.commit()
    db.refresh(annonce)
    
    return annonce


@router.put("/{annonce_id}", response_model=AnnonceResponse)
def update_annonce(
    annonce_id: int,
    annonce_data: AnnonceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an annonce"""
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    # Check ownership
    if annonce.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this annonce"
        )
    
    # Update fields
    for field, value in annonce_data.dict(exclude_unset=True).items():
        setattr(annonce, field, value)
    
    db.commit()
    db.refresh(annonce)
    
    return annonce


@router.delete("/{annonce_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_annonce(
    annonce_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an annonce"""
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    # Check ownership
    if annonce.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this annonce"
        )
    
    # Delete images from storage
    for image in annonce.images:
        upload_service.delete_file(image.url)
    
    # Delete annonce (cascade will delete images)
    db.delete(annonce)
    db.commit()
    
    return None


@router.get("/user/{user_id}", response_model=List[AnnonceListResponse])
def list_user_annonces(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List annonces by user"""
    annonces = db.query(Annonce)\
        .filter(and_(Annonce.user_id == user_id, Annonce.status == AnnonceStatus.ACTIVE))\
        .order_by(Annonce.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return annonces
