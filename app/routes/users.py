"""
User routes (profile, dashboard)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict
from app.models import UserProfile
from app.security import get_current_user, require_role
from app.database import get_users_collection

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: Dict = Depends(get_current_user)):
    """Get current user profile (requires authentication)"""
    users_collection = get_users_collection()
    
    db_user = users_collection.find_one({"email": current_user["sub"]})
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserProfile(
        email=db_user["email"],
        full_name=db_user["full_name"],
        role=db_user["role"],
        created_at=db_user["created_at"],
        is_active=db_user.get("is_active", True)
    )


@router.get("/dashboard")
async def user_dashboard(current_user: Dict = Depends(require_role("user"))):
    """User-only dashboard endpoint"""
    return {
        "message": f"Welcome {current_user['sub']}",
        "role": current_user.get("role"),
        "data": "This is user-only information"
    }


@router.get("/all", response_model=list)
async def get_all_users(current_user: Dict = Depends(require_role("doctor"))):
    """Get all users (doctor only)"""
    users_collection = get_users_collection()
    
    users = list(users_collection.find(
        {},
        {"password": 0, "_id": 0}  # Exclude password and MongoDB ID
    ))
    
    return users
