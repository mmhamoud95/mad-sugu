from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...api.deps import get_db, get_current_user
from ...models import Alert, User, Category
from ...schemas.alert import AlertCreate, Alert as AlertSchema, AlertUpdate

router = APIRouter()


@router.post("/", response_model=AlertSchema, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new alert for the current user
    """
    # Validate category if provided
    if alert.category_id:
        category = db.query(Category).filter(Category.id == alert.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Create alert
    db_alert = Alert(
        **alert.model_dump(),
        user_id=current_user.id
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    return db_alert


@router.get("/", response_model=List[AlertSchema])
def get_my_alerts(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all alerts for the current user
    """
    alerts = db.query(Alert).filter(
        Alert.user_id == current_user.id
    ).order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    return alerts


@router.get("/{alert_id}", response_model=AlertSchema)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific alert
    """
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert


@router.put("/{alert_id}", response_model=AlertSchema)
def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an alert
    """
    db_alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Validate category if provided
    if alert_update.category_id:
        category = db.query(Category).filter(Category.id == alert_update.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Update alert
    update_data = alert_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    
    return db_alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an alert
    """
    db_alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    db.delete(db_alert)
    db.commit()
    
    return None


@router.post("/{alert_id}/toggle", response_model=AlertSchema)
def toggle_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle alert active status
    """
    db_alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    db_alert.is_active = not db_alert.is_active
    db.commit()
    db.refresh(db_alert)
    
    return db_alert
