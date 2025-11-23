from sqlalchemy.orm import Session
from typing import Optional
from ..models import Notification, NotificationType, User, Annonce


class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        notification_type: NotificationType,
        title: str,
        message: str,
        annonce_id: Optional[int] = None,
        related_user_id: Optional[int] = None
    ) -> Notification:
        """
        Create a new notification
        """
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            annonce_id=annonce_id,
            related_user_id=related_user_id
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    
    @staticmethod
    def notify_new_message(
        db: Session,
        receiver_id: int,
        sender_name: str,
        annonce_title: str,
        annonce_id: int
    ):
        """Create notification for new message"""
        return NotificationService.create_notification(
            db=db,
            user_id=receiver_id,
            notification_type=NotificationType.NEW_MESSAGE,
            title="Nouveau message",
            message=f"{sender_name} vous a envoyé un message concernant '{annonce_title}'",
            annonce_id=annonce_id
        )
    
    @staticmethod
    def notify_new_favorite(
        db: Session,
        annonce_owner_id: int,
        annonce_title: str,
        annonce_id: int
    ):
        """Create notification for new favorite"""
        return NotificationService.create_notification(
            db=db,
            user_id=annonce_owner_id,
            notification_type=NotificationType.NEW_FAVORITE,
            title="Nouveau favori",
            message=f"Votre annonce '{annonce_title}' a été ajoutée aux favoris",
            annonce_id=annonce_id
        )
    
    @staticmethod
    def notify_new_review(
        db: Session,
        user_id: int,
        reviewer_name: str,
        rating: float
    ):
        """Create notification for new review"""
        stars = "⭐" * int(rating)
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            notification_type=NotificationType.NEW_REVIEW,
            title="Nouvelle évaluation",
            message=f"{reviewer_name} vous a donné {stars} ({rating}/5)"
        )
    
    @staticmethod
    def notify_alert_matched(
        db: Session,
        user_id: int,
        alert_title: str,
        annonce_title: str,
        annonce_id: int
    ):
        """Create notification for matched alert"""
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            notification_type=NotificationType.ALERT_MATCHED,
            title="Alerte correspondante",
            message=f"Une nouvelle annonce correspond à votre alerte '{alert_title}': {annonce_title}",
            annonce_id=annonce_id
        )
    
    @staticmethod
    def notify_annonce_expired(
        db: Session,
        user_id: int,
        annonce_title: str,
        annonce_id: int
    ):
        """Create notification for expired annonce"""
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            notification_type=NotificationType.ANNONCE_EXPIRED,
            title="Annonce expirée",
            message=f"Votre annonce '{annonce_title}' a expiré. Vous pouvez la renouveler.",
            annonce_id=annonce_id
        )
    
    @staticmethod
    def notify_boost_expired(
        db: Session,
        user_id: int,
        annonce_title: str,
        annonce_id: int
    ):
        """Create notification for expired boost"""
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            notification_type=NotificationType.BOOST_EXPIRED,
            title="Boost expiré",
            message=f"Le boost de votre annonce '{annonce_title}' a expiré",
            annonce_id=annonce_id
        )
