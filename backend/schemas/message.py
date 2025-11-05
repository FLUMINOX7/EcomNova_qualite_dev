"""Pydantic schemas for messages"""

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """Create a message in a thread"""

    body: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    """Message response"""

    id: str
    thread_id: str
    author_user_id: str | None  # None = support agent
    body: str
    created_at: float

    class Config:
        from_attributes = True


class ThreadCreate(BaseModel):
    """Create a new message thread"""

    subject: str = Field(..., min_length=1, max_length=200)
    order_id: str | None = None
    initial_message: str = Field(..., min_length=1, max_length=5000)


class ThreadResponse(BaseModel):
    """Thread response with messages"""

    id: str
    user_id: str
    order_id: str | None
    subject: str
    closed: bool
    created_at: float
    messages: list[MessageResponse] = []

    class Config:
        from_attributes = True
