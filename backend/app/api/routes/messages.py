from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List
from datetime import datetime
from ...core.database import get_db
from ...api.deps import get_current_active_user
from ...models import Message, User, Annonce
from ...schemas import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/", response_model=List[MessageResponse])
def list_messages(
    annonce_id: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List messages for current user"""
    query = db.query(Message).filter(
        or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    )
    
    # Filter by annonce if provided
    if annonce_id:
        query = query.filter(Message.annonce_id == annonce_id)
    
    messages = query.order_by(Message.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return messages


@router.get("/conversations")
def list_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all conversations for current user"""
    # Get all messages where user is sender or receiver
    messages = db.query(Message).filter(
        or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    ).order_by(Message.created_at.desc()).all()
    
    # Group by annonce and other user
    conversations = {}
    for msg in messages:
        other_user_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        key = (msg.annonce_id, other_user_id)
        
        if key not in conversations:
            conversations[key] = {
                "annonce_id": msg.annonce_id,
                "other_user_id": other_user_id,
                "last_message": msg.content,
                "last_message_at": msg.created_at,
                "unread_count": 0
            }
        
        # Count unread messages
        if msg.receiver_id == current_user.id and not msg.is_read:
            conversations[key]["unread_count"] += 1
    
    return list(conversations.values())


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send a message"""
    # Verify annonce exists
    annonce = db.query(Annonce).filter(Annonce.id == message_data.annonce_id).first()
    if not annonce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annonce not found"
        )
    
    # Verify receiver exists
    receiver = db.query(User).filter(User.id == message_data.receiver_id).first()
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    
    # Cannot send message to self
    if message_data.receiver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send message to yourself"
        )
    
    # Create message
    message = Message(
        content=message_data.content,
        sender_id=current_user.id,
        receiver_id=message_data.receiver_id,
        annonce_id=message_data.annonce_id
    )
    db.add(message)
    
    # Increment messages count on annonce
    annonce.messages_count += 1
    
    db.commit()
    db.refresh(message)
    
    return message


@router.put("/{message_id}/read", response_model=MessageResponse)
def mark_message_read(
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a message as read"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Only receiver can mark as read
    if message.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to mark this message as read"
        )
    
    message.is_read = True
    message.read_at = datetime.utcnow()
    db.commit()
    db.refresh(message)
    
    return message


@router.get("/annonce/{annonce_id}/conversation/{other_user_id}", response_model=List[MessageResponse])
def get_conversation(
    annonce_id: int,
    other_user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get conversation between current user and another user for a specific annonce"""
    messages = db.query(Message).filter(
        and_(
            Message.annonce_id == annonce_id,
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == other_user_id),
                and_(Message.sender_id == other_user_id, Message.receiver_id == current_user.id)
            )
        )
    ).order_by(Message.created_at.asc()).all()
    
    # Mark unread messages as read
    for msg in messages:
        if msg.receiver_id == current_user.id and not msg.is_read:
            msg.is_read = True
            msg.read_at = datetime.utcnow()
    
    db.commit()
    
    return messages
