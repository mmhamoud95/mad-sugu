from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...api.deps import get_current_active_user
from ...models import Favorite, User, Annonce
from ...schemas import AnnonceListResponse

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/", response_model=List[AnnonceListResponse])
def list_favorites(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's favorite annonces"""
    favorites = db.query(Favorite)\
        .filter(Favorite.user_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    annonces = [fav.annonce for fav in favorites]
    return annonces


@router.post("/{annonce_id}", status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    annonce_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add annonce to favorites"""
    # Check if annonce exists
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    # Check if already favorited
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.annonce_id == annonce_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Annonce already in favorites"
        )
    
    # Add to favorites
    favorite = Favorite(user_id=current_user.id, annonce_id=annonce_id)
    db.add(favorite)
    
    # Increment favorites count
    annonce.favorites_count += 1
    
    db.commit()
    
    return {"message": "Added to favorites"}


@router.delete("/{annonce_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_favorites(
    annonce_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove annonce from favorites"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.annonce_id == annonce_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    # Get annonce to decrement count
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if annonce and annonce.favorites_count > 0:
        annonce.favorites_count -= 1
    
    db.delete(favorite)
    db.commit()
    
    return None


@router.get("/check/{annonce_id}")
def check_favorite(
    annonce_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Check if annonce is in user's favorites"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.annonce_id == annonce_id
    ).first()
    
    return {"is_favorite": favorite is not None}
