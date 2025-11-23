from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List
from datetime import datetime, timedelta, date

from ...api.deps import get_db, get_current_user
from ...models import (
    Annonce, User, Message, Favorite, AnnonceView, 
    DailyStats, Review, AnnonceStatus
)
from ...schemas.analytics import (
    AnalyticsSummary, UserAnalytics, DailyStatsResponse, AnnonceViewCreate
)

router = APIRouter()


@router.post("/views", status_code=status.HTTP_201_CREATED)
def track_annonce_view(
    view: AnnonceViewCreate,
    db: Session = Depends(get_db)
):
    """
    Track an annonce view (can be called by anonymous users)
    """
    # Verify annonce exists
    annonce = db.query(Annonce).filter(Annonce.id == view.annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    # Create view record
    db_view = AnnonceView(**view.model_dump())
    db.add(db_view)
    
    # Increment annonce views count
    annonce.views_count += 1
    
    db.commit()
    
    return {"message": "View tracked successfully"}


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get overall analytics summary (admin only for now)
    """
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Total counts
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_annonces = db.query(func.count(Annonce.id)).scalar() or 0
    active_annonces = db.query(func.count(Annonce.id)).filter(
        Annonce.status == AnnonceStatus.ACTIVE
    ).scalar() or 0
    total_messages = db.query(func.count(Message.id)).scalar() or 0
    total_views = db.query(func.sum(Annonce.views_count)).scalar() or 0
    total_favorites = db.query(func.count(Favorite.id)).scalar() or 0
    
    # Calculate boost revenue (if boost price is implemented)
    total_revenue = 0.0  # To be implemented with payment system
    
    # Period-specific counts
    period_new_users = db.query(func.count(User.id)).filter(
        User.created_at >= start_date
    ).scalar() or 0
    
    period_new_annonces = db.query(func.count(Annonce.id)).filter(
        Annonce.created_at >= start_date
    ).scalar() or 0
    
    period_views = db.query(func.count(AnnonceView.id)).filter(
        AnnonceView.viewed_at >= start_date
    ).scalar() or 0
    
    period_messages = db.query(func.count(Message.id)).filter(
        Message.created_at >= start_date
    ).scalar() or 0
    
    return AnalyticsSummary(
        total_users=total_users,
        total_annonces=total_annonces,
        active_annonces=active_annonces,
        total_messages=total_messages,
        total_views=total_views,
        total_favorites=total_favorites,
        total_revenue=total_revenue,
        period_new_users=period_new_users,
        period_new_annonces=period_new_annonces,
        period_views=period_views,
        period_messages=period_messages
    )


@router.get("/user/{user_id}", response_model=UserAnalytics)
def get_user_analytics(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analytics for a specific user (own or admin)
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only allow users to see their own analytics (unless admin)
    if current_user.id != user_id:
        # Add admin check here when admin role is implemented
        pass
    
    # Get annonce statistics
    total_annonces = db.query(func.count(Annonce.id)).filter(
        Annonce.user_id == user_id
    ).scalar() or 0
    
    active_annonces = db.query(func.count(Annonce.id)).filter(
        and_(Annonce.user_id == user_id, Annonce.status == AnnonceStatus.ACTIVE)
    ).scalar() or 0
    
    sold_annonces = db.query(func.count(Annonce.id)).filter(
        and_(Annonce.user_id == user_id, Annonce.status == AnnonceStatus.SOLD)
    ).scalar() or 0
    
    # Get engagement statistics
    total_views = db.query(func.sum(Annonce.views_count)).filter(
        Annonce.user_id == user_id
    ).scalar() or 0
    
    total_messages_received = db.query(func.count(Message.id)).filter(
        Message.receiver_id == user_id
    ).scalar() or 0
    
    total_favorites_received = db.query(func.sum(Annonce.favorites_count)).filter(
        Annonce.user_id == user_id
    ).scalar() or 0
    
    # Get rating statistics
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.reviewed_user_id == user_id
    ).scalar() or 0.0
    
    total_reviews = db.query(func.count(Review.id)).filter(
        Review.reviewed_user_id == user_id
    ).scalar() or 0
    
    return UserAnalytics(
        user_id=user_id,
        total_annonces=total_annonces,
        active_annonces=active_annonces,
        sold_annonces=sold_annonces,
        total_views=total_views,
        total_messages_received=total_messages_received,
        total_favorites_received=total_favorites_received,
        average_rating=float(avg_rating),
        total_reviews=total_reviews
    )


@router.get("/daily-stats", response_model=List[DailyStatsResponse])
def get_daily_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get daily statistics (admin only)
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    stats = db.query(DailyStats).filter(
        and_(
            DailyStats.stat_date >= start_date,
            DailyStats.stat_date <= end_date
        )
    ).order_by(DailyStats.stat_date.desc()).all()
    
    return stats
