from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..models import Alert, Annonce, AnnonceStatus
from .notification_service import NotificationService


class AlertService:
    """Service for managing alerts and matching them with new annonces"""
    
    @staticmethod
    def check_alerts_for_annonce(db: Session, annonce: Annonce) -> List[Alert]:
        """
        Check all active alerts to see if they match the given annonce
        Returns list of matched alerts
        """
        matched_alerts = []
        
        # Get all active alerts
        alerts = db.query(Alert).filter(Alert.is_active == True).all()
        
        for alert in alerts:
            if AlertService._matches_alert(annonce, alert):
                matched_alerts.append(alert)
                
                # Update last_triggered
                alert.last_triggered = datetime.utcnow()
                
                # Send notification to user
                NotificationService.notify_alert_matched(
                    db=db,
                    user_id=alert.user_id,
                    alert_title=alert.title,
                    annonce_title=annonce.title,
                    annonce_id=annonce.id
                )
        
        if matched_alerts:
            db.commit()
        
        return matched_alerts
    
    @staticmethod
    def _matches_alert(annonce: Annonce, alert: Alert) -> bool:
        """
        Check if an annonce matches an alert's criteria
        """
        # Check if annonce is active
        if annonce.status != AnnonceStatus.ACTIVE:
            return False
        
        # Check category
        if alert.category_id and annonce.category_id != alert.category_id:
            return False
        
        # Check location
        if alert.location_city and annonce.location_city:
            if alert.location_city.lower() != annonce.location_city.lower():
                return False
        
        # Check price range
        if alert.min_price and annonce.price < alert.min_price:
            return False
        
        if alert.max_price and annonce.price > alert.max_price:
            return False
        
        # Check keywords
        if alert.keywords:
            keywords = alert.keywords.lower().split()
            annonce_text = f"{annonce.title} {annonce.description}".lower()
            
            # Check if any keyword matches
            if not any(keyword in annonce_text for keyword in keywords):
                return False
        
        return True
