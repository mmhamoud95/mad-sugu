from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import List, Optional
from datetime import datetime, timedelta

from ...api.deps import get_db, get_current_user
from ...models import (
    User, Annonce, AnnonceStatus, Review, Message, 
    Notification, NotificationType
)
from ...schemas.annonce import Annonce as AnnonceSchema
from ...schemas.user import User as UserSchema

router = APIRouter()


def is_admin(user: User) -> bool:
    """
    Check if user is admin (placeholder - implement proper admin role)
    """
    # For now, we can check for a specific field or email
    # TODO: Implement proper role-based access control
    return user.is_pro  # Temporary: using is_pro as admin flag


def require_admin(current_user: User = Depends(get_current_user)):
    """
    Dependency to require admin access
    """
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("/users", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    is_verified: Optional[bool] = None,
    is_pro: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    List all users (admin only)
    """
    query = db.query(User)
    
    if search:
        query = query.filter(
            or_(
                User.email.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%")
            )
        )
    
    if is_verified is not None:
        query = query.filter(User.is_verified == is_verified)
    
    if is_pro is not None:
        query = query.filter(User.is_pro == is_pro)
    
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    
    return users


@router.put("/users/{user_id}/verify")
def verify_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Verify a user account (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_verified = True
    db.commit()
    
    return {"message": "User verified successfully"}


@router.put("/users/{user_id}/suspend")
def suspend_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Suspend a user account (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    
    return {"message": "User suspended successfully"}


@router.get("/annonces/pending", response_model=List[AnnonceSchema])
def list_pending_annonces(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    List annonces pending moderation (admin only)
    """
    annonces = db.query(Annonce).filter(
        Annonce.status == AnnonceStatus.DRAFT
    ).order_by(Annonce.created_at.desc()).offset(skip).limit(limit).all()
    
    return annonces


@router.put("/annonces/{annonce_id}/approve")
def approve_annonce(
    annonce_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Approve an annonce (admin only)
    """
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    annonce.status = AnnonceStatus.ACTIVE
    db.commit()
    
    # Send notification to user
    notification = Notification(
        user_id=annonce.user_id,
        type=NotificationType.ADMIN_MESSAGE,
        title="Annonce approuvée",
        message=f"Votre annonce '{annonce.title}' a été approuvée et est maintenant active.",
        annonce_id=annonce.id
    )
    db.add(notification)
    db.commit()
    
    return {"message": "Annonce approved successfully"}


@router.put("/annonces/{annonce_id}/disable")
def disable_annonce(
    annonce_id: int,
    reason: str = Query(..., description="Reason for disabling"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Disable an annonce (admin only)
    """
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    annonce.status = AnnonceStatus.DISABLED
    db.commit()
    
    # Send notification to user
    notification = Notification(
        user_id=annonce.user_id,
        type=NotificationType.ADMIN_MESSAGE,
        title="Annonce désactivée",
        message=f"Votre annonce '{annonce.title}' a été désactivée. Raison: {reason}",
        annonce_id=annonce.id
    )
    db.add(notification)
    db.commit()
    
    return {"message": "Annonce disabled successfully"}


@router.get("/stats/dashboard")
def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get dashboard statistics for admin (admin only)
    """
    # Total counts
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_annonces = db.query(func.count(Annonce.id)).scalar() or 0
    active_annonces = db.query(func.count(Annonce.id)).filter(
        Annonce.status == AnnonceStatus.ACTIVE
    ).scalar() or 0
    pending_annonces = db.query(func.count(Annonce.id)).filter(
        Annonce.status == AnnonceStatus.DRAFT
    ).scalar() or 0
    
    # Recent activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    new_users_7d = db.query(func.count(User.id)).filter(
        User.created_at >= seven_days_ago
    ).scalar() or 0
    
    new_annonces_7d = db.query(func.count(Annonce.id)).filter(
        Annonce.created_at >= seven_days_ago
    ).scalar() or 0
    
    new_messages_7d = db.query(func.count(Message.id)).filter(
        Message.created_at >= seven_days_ago
    ).scalar() or 0
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    new_users_30d = db.query(func.count(User.id)).filter(
        User.created_at >= thirty_days_ago
    ).scalar() or 0
    
    new_annonces_30d = db.query(func.count(Annonce.id)).filter(
        Annonce.created_at >= thirty_days_ago
    ).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_annonces": total_annonces,
        "active_annonces": active_annonces,
        "pending_annonces": pending_annonces,
        "new_users_7d": new_users_7d,
        "new_annonces_7d": new_annonces_7d,
        "new_messages_7d": new_messages_7d,
        "new_users_30d": new_users_30d,
        "new_annonces_30d": new_annonces_30d
    }


@router.delete("/reviews/{review_id}")
def delete_review_admin(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete any review (admin only)
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    db.delete(review)
    db.commit()
    
    return {"message": "Review deleted successfully"}
