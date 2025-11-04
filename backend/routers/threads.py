"""Message and support thread endpoints"""
from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.dependencies import get_session
from backend.schemas.message import ThreadCreate, ThreadResponse, MessageCreate, MessageResponse
from backend.repositories.message import MessageRepository
from backend.auth.jwt import get_current_user_id, require_admin

router = APIRouter(prefix="/threads", tags=["Support"])


def _build_thread_response(thread) -> ThreadResponse:
    """Helper to build thread response with messages"""
    messages_response = [
        MessageResponse(
            id=msg.id,
            thread_id=msg.thread_id,
            author_user_id=msg.author_user_id,
            body=msg.body,
            created_at=msg.created_at
        )
        for msg in thread.messages
    ]
    
    return ThreadResponse(
        id=thread.id,
        user_id=thread.user_id,
        order_id=thread.order_id,
        subject=thread.subject,
        closed=thread.closed,
        created_at=thread.created_at,
        messages=messages_response
    )


@router.post("", response_model=ThreadResponse, status_code=status.HTTP_201_CREATED)
def create_thread(
    thread_data: ThreadCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Create a new support thread"""
    repo = MessageRepository(db)
    
    # Create thread
    thread = repo.create_thread(
        user_id=user_id,
        subject=thread_data.subject,
        order_id=thread_data.order_id
    )
    
    # Add initial message
    repo.add_message(
        thread_id=thread.id,
        body=thread_data.initial_message,
        author_user_id=user_id
    )
    
    # Refresh to get messages
    db.refresh(thread)
    
    return _build_thread_response(thread)


@router.get("", response_model=List[ThreadResponse])
def list_threads(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """List current user's support threads"""
    repo = MessageRepository(db)
    threads = repo.list_user_threads(user_id)
    return [_build_thread_response(t) for t in threads]


@router.get("/admin/all", response_model=List[ThreadResponse])
def list_all_threads(
    admin_id: str = Depends(require_admin),
    db: Session = Depends(get_session)
):
    """List all support threads (admin only)"""
    repo = MessageRepository(db)
    threads = repo.list_all_threads()
    return [_build_thread_response(t) for t in threads]


@router.get("/{thread_id}", response_model=ThreadResponse)
def get_thread(
    thread_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Get a specific thread"""
    repo = MessageRepository(db)
    thread = repo.get_thread_by_id(thread_id)
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )
    
    # Verify ownership (or admin)
    if thread.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this thread"
        )
    
    return _build_thread_response(thread)


@router.post("/{thread_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def post_message(
    thread_id: str,
    message_data: MessageCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Post a message to a thread"""
    repo = MessageRepository(db)
    thread = repo.get_thread_by_id(thread_id)
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )
    
    if thread.closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Thread is closed"
        )
    
    # Verify ownership
    if thread.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to post in this thread"
        )
    
    message = repo.add_message(
        thread_id=thread_id,
        body=message_data.body,
        author_user_id=user_id
    )
    
    return message


@router.post("/{thread_id}/close", response_model=ThreadResponse)
def close_thread(
    thread_id: str,
    admin_id: str = Depends(require_admin),
    db: Session = Depends(get_session)
):
    """Close a support thread (admin only)"""
    repo = MessageRepository(db)
    thread = repo.close_thread(thread_id)
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )
    
    return _build_thread_response(thread)


@router.post("/{thread_id}/admin-reply", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def admin_reply(
    thread_id: str,
    message_data: MessageCreate,
    admin_id: str = Depends(require_admin),
    db: Session = Depends(get_session)
):
    """Admin replies to a thread (author_user_id = None)"""
    repo = MessageRepository(db)
    thread = repo.get_thread_by_id(thread_id)
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found"
        )
    
    # Admin message with author_user_id = None
    message = repo.add_message(
        thread_id=thread_id,
        body=message_data.body,
        author_user_id=None  # None = support agent
    )
    
    return message
