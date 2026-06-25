"""
Authentication routes (register, login)
"""
from fastapi import APIRouter, HTTPException, status
from app.models import UserRegister, UserLogin, TokenResponse, UserResponse
from app.security import hash_password, verify_password, create_access_token
from app.database import get_users_collection
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserRegister):
    """Register a new user with role (doctor or user)"""
    users_collection = get_users_collection()
    
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_doc = {
        "email": user.email,
        "full_name": user.full_name,
        "password": hash_password(user.password),
        "role": user.role,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True
    }
    
    users_collection.insert_one(user_doc)
    
    return UserResponse(
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        created_at=user_doc["created_at"]
    )


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    """Login user and return JWT token"""
    users_collection = get_users_collection()
    
    # Find user in database
    db_user = users_collection.find_one({"email": user.email})
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not db_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    
    # Generate token
    access_token = create_access_token(
        email=db_user["email"],
        role=db_user["role"]
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=db_user["role"]
    )
