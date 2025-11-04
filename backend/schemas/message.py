"""Pydantic schemas for messages"""
from pydantic import BaseModel, Field
from typing import List, Optional


class MessageCreate(BaseModel):
    """Create a message in a thread"""
    body: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    """Message response"""
    id: str
    thread_id: str
    author_user_id: Optional[str]  # None = support agent
    body: str
    created_at: float

    class Config:
        from_attributes = True


class ThreadCreate(BaseModel):
    """Create a new message thread"""
    subject: str = Field(..., min_length=1, max_length=200)
    order_id: Optional[str] = None
    initial_message: str = Field(..., min_length=1, max_length=5000)


class ThreadResponse(BaseModel):
    """Thread response with messages"""
    id: str
    user_id: str
    order_id: Optional[str]
    subject: str
    closed: bool
    created_at: float
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True
