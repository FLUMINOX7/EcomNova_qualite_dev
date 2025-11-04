"""User repository for database operations"""
from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from backend.models_sql import UserModel
from backend.auth.jwt import hash_password
import uuid


class UserRepository:
    """Repository for user operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        address: str,
        is_admin: bool = False
    ) -> UserModel:
        """Create a new user"""
        user = UserModel(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=hash_password(password),
            first_name=first_name,
            last_name=last_name,
            address=address,
            is_admin=is_admin
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get a user by email"""
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        """Get a user by ID"""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.db.query(UserModel).filter(UserModel.email == email).first() is not None

    def update_user(
        self,
        user_id: str,
        *,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Optional[UserModel]:
        """Update user fields; returns updated user or None if not found.
        If email is provided and changed, ensures uniqueness.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        if email is not None and email != user.email:
            # enforce email uniqueness
            if self.email_exists(email):
                raise ValueError("Email already registered")
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if address is not None:
            user.address = address

        self.db.commit()
        self.db.refresh(user)
        return user
