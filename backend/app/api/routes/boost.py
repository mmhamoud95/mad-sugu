from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

from ...api.deps import get_db, get_current_user
from ...models import Annonce, User, AnnonceStatus
from ...services.notification_service import NotificationService

router = APIRouter()


class BoostCreate(BaseModel):
    annonce_id: int
    duration_days: int = 7  # Duration in days (7, 14, 30)


class BoostPrice(BaseModel):
    duration_days: int
    price: float
    currency: str = "FCFA"


@router.get("/prices")
def get_boost_prices():
    """
    Get boost pricing information
    """
    prices = [
        {"duration_days": 7, "price": 2000, "currency": "FCFA", "label": "7 jours"},
        {"duration_days": 14, "price": 3500, "currency": "FCFA", "label": "14 jours"},
        {"duration_days": 30, "price": 6000, "currency": "FCFA", "label": "30 jours"}
    ]
    return {"prices": prices}


@router.post("/", status_code=status.HTTP_201_CREATED)
def boost_annonce(
    boost: BoostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Boost an annonce (make it featured)
    In production, this would require payment integration
    """
    # Verify annonce exists and belongs to user
    annonce = db.query(Annonce).filter(
        Annonce.id == boost.annonce_id,
        Annonce.user_id == current_user.id
    ).first()
    
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found or you don't have permission"
        )
    
    # Check if annonce is active
    if annonce.status != AnnonceStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only active annonces can be boosted"
        )
    
    # Validate duration
    if boost.duration_days not in [7, 14, 30]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duration must be 7, 14, or 30 days"
        )
    
    # TODO: Integrate with payment system (Mobile Money)
    # For now, we'll just apply the boost directly
    
    # Calculate boost end date
    boost_end = datetime.utcnow() + timedelta(days=boost.duration_days)
    
    # Apply boost
    annonce.is_featured = True
    annonce.featured_until = boost_end
    
    db.commit()
    db.refresh(annonce)
    
    return {
        "message": "Annonce boosted successfully",
        "annonce_id": annonce.id,
        "featured_until": boost_end,
        "duration_days": boost.duration_days
    }


@router.delete("/{annonce_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_boost(
    annonce_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove boost from an annonce
    """
    annonce = db.query(Annonce).filter(
        Annonce.id == annonce_id,
        Annonce.user_id == current_user.id
    ).first()
    
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found or you don't have permission"
        )
    
    annonce.is_featured = False
    annonce.featured_until = None
    
    db.commit()
    
    return None


@router.get("/my-boosted")
def get_my_boosted_annonces(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all boosted annonces for current user
    """
    annonces = db.query(Annonce).filter(
        Annonce.user_id == current_user.id,
        Annonce.is_featured == True,
        Annonce.featured_until > datetime.utcnow()
    ).order_by(Annonce.featured_until.desc()).offset(skip).limit(limit).all()
    
    return annonces


@router.post("/{annonce_id}/urgent")
def mark_as_urgent(
    annonce_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark annonce as urgent (free feature)
    """
    annonce = db.query(Annonce).filter(
        Annonce.id == annonce_id,
        Annonce.user_id == current_user.id
    ).first()
    
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found or you don't have permission"
        )
    
    annonce.is_urgent = True
    db.commit()
    
    return {"message": "Annonce marked as urgent"}


@router.delete("/{annonce_id}/urgent", status_code=status.HTTP_204_NO_CONTENT)
def remove_urgent(
    annonce_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove urgent flag from annonce
    """
    annonce = db.query(Annonce).filter(
        Annonce.id == annonce_id,
        Annonce.user_id == current_user.id
    ).first()
    
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found or you don't have permission"
        )
    
    annonce.is_urgent = False
    db.commit()
    
    return None
