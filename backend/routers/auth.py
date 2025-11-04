"""Authentication endpoints"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.dependencies import get_session
from backend.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse, UserUpdate
from backend.repositories.user import UserRepository
from backend.auth.jwt import verify_password, create_access_token, get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_session)):
    """Register a new user"""
    repo = UserRepository(db)
    
    # Check if email already exists
    if repo.email_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = repo.create_user(
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        address=user_data.address
    )
    
    # Generate token
    access_token = create_access_token(
        data={"sub": user.id, "is_admin": user.is_admin}
    )
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_session)):
    """Login user"""
    repo = UserRepository(db)
    
    # Get user by email
    user = repo.get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate token
    access_token = create_access_token(
        data={"sub": user.id, "is_admin": user.is_admin}
    )
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Get current authenticated user"""
    repo = UserRepository(db)
    user = repo.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)


@router.put("/me", response_model=UserResponse)
def update_current_user(
    update: UserUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Update current authenticated user's personal information"""
    repo = UserRepository(db)
    try:
        user = repo.update_user(
            user_id,
            email=update.email,
            first_name=update.first_name,
            last_name=update.last_name,
            address=update.address,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse.from_orm(user)
