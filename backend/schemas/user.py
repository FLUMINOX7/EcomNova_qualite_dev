"""User-related Pydantic schemas"""
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(min_length=6)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    address: str = Field(min_length=1)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: str
    email: str
    first_name: str
    last_name: str
    address: str
    is_admin: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
