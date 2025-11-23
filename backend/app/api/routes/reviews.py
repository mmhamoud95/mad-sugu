from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ...api.deps import get_db, get_current_user
from ...models import Review, User
from ...schemas.review import ReviewCreate, Review as ReviewSchema, ReviewUpdate

router = APIRouter()


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new review for a user
    """
    # Check if reviewed user exists
    reviewed_user = db.query(User).filter(User.id == review.reviewed_user_id).first()
    if not reviewed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent self-review
    if current_user.id == review.reviewed_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot review yourself"
        )
    
    # Check if user already reviewed this user
    existing_review = db.query(Review).filter(
        Review.reviewer_id == current_user.id,
        Review.reviewed_user_id == review.reviewed_user_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this user"
        )
    
    # Create review
    db_review = Review(
        **review.model_dump(),
        reviewer_id=current_user.id
    )
    db.add(db_review)
    
    # Update user rating
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.reviewed_user_id == review.reviewed_user_id
    ).scalar() or 0.0
    
    review_count = db.query(func.count(Review.id)).filter(
        Review.reviewed_user_id == review.reviewed_user_id
    ).scalar() or 0
    
    reviewed_user.rating = float(avg_rating)
    reviewed_user.rating_count = review_count + 1
    
    db.commit()
    db.refresh(db_review)
    
    return db_review


@router.get("/user/{user_id}", response_model=List[ReviewSchema])
def get_user_reviews(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a specific user
    """
    reviews = db.query(Review).filter(
        Review.reviewed_user_id == user_id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews


@router.get("/my-reviews", response_model=List[ReviewSchema])
def get_my_reviews(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get reviews given by the current user
    """
    reviews = db.query(Review).filter(
        Review.reviewer_id == current_user.id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews


@router.put("/{review_id}", response_model=ReviewSchema)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a review (only by the reviewer)
    """
    db_review = db.query(Review).filter(Review.id == review_id).first()
    
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if db_review.reviewer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this review"
        )
    
    # Update review
    update_data = review_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    
    # Recalculate user rating if rating changed
    if "rating" in update_data:
        avg_rating = db.query(func.avg(Review.rating)).filter(
            Review.reviewed_user_id == db_review.reviewed_user_id
        ).scalar() or 0.0
        
        reviewed_user = db.query(User).filter(User.id == db_review.reviewed_user_id).first()
        if reviewed_user:
            reviewed_user.rating = float(avg_rating)
            db.commit()
    
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a review (only by the reviewer)
    """
    db_review = db.query(Review).filter(Review.id == review_id).first()
    
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if db_review.reviewer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    reviewed_user_id = db_review.reviewed_user_id
    
    db.delete(db_review)
    db.commit()
    
    # Recalculate user rating
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.reviewed_user_id == reviewed_user_id
    ).scalar() or 0.0
    
    review_count = db.query(func.count(Review.id)).filter(
        Review.reviewed_user_id == reviewed_user_id
    ).scalar() or 0
    
    reviewed_user = db.query(User).filter(User.id == reviewed_user_id).first()
    if reviewed_user:
        reviewed_user.rating = float(avg_rating)
        reviewed_user.rating_count = review_count
        db.commit()
    
    return None
