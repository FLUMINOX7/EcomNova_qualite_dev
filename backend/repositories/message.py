"""Message and thread repository for database operations"""
from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models_sql import MessageThreadModel, MessageModel
import uuid
import time


class MessageRepository:
    """Repository for message operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_thread(
        self,
        user_id: str,
        subject: str,
        order_id: Optional[str] = None
    ) -> MessageThreadModel:
        """Create a new message thread"""
        thread = MessageThreadModel(
            id=str(uuid.uuid4()),
            user_id=user_id,
            order_id=order_id,
            subject=subject,
            closed=False,
            created_at=time.time()
        )
        self.db.add(thread)
        self.db.commit()
        self.db.refresh(thread)
        return thread
    
    def get_thread_by_id(self, thread_id: str) -> Optional[MessageThreadModel]:
        """Get a thread by ID"""
        return self.db.query(MessageThreadModel).filter(
            MessageThreadModel.id == thread_id
        ).first()
    
    def list_user_threads(self, user_id: str) -> List[MessageThreadModel]:
        """Get all threads for a user"""
        return self.db.query(MessageThreadModel).filter(
            MessageThreadModel.user_id == user_id
        ).order_by(MessageThreadModel.created_at.desc()).all()
    
    def list_all_threads(self) -> List[MessageThreadModel]:
        """Get all threads (admin only)"""
        return self.db.query(MessageThreadModel).order_by(
            MessageThreadModel.created_at.desc()
        ).all()
    
    def add_message(
        self,
        thread_id: str,
        body: str,
        author_user_id: Optional[str] = None
    ) -> MessageModel:
        """Add a message to a thread"""
        message = MessageModel(
            id=str(uuid.uuid4()),
            thread_id=thread_id,
            author_user_id=author_user_id,
            body=body,
            created_at=time.time()
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def close_thread(self, thread_id: str) -> Optional[MessageThreadModel]:
        """Close a thread (admin only)"""
        thread = self.get_thread_by_id(thread_id)
        if thread:
            thread.closed = True
            self.db.commit()
            self.db.refresh(thread)
        return thread
