"""
Doctor-specific routes
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict
from app.security import require_role
from app.database import get_users_collection

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])


@router.get("/dashboard")
async def doctor_dashboard(current_user: Dict = Depends(require_role("doctor"))):
    """Doctor-only dashboard endpoint"""
    return {
        "message": f"Welcome Dr. {current_user['sub']}",
        "role": "doctor",
        "data": "This is doctor-only information"
    }


@router.get("/stats")
async def get_doctor_stats(current_user: Dict = Depends(require_role("doctor"))):
    """Get system statistics (doctor only)"""
    users_collection = get_users_collection()
    
    total_users = users_collection.count_documents({})
    total_doctors = users_collection.count_documents({"role": "doctor"})
    total_patients = users_collection.count_documents({"role": "user"})
    
    return {
        "total_users": total_users,
        "total_doctors": total_doctors,
        "total_patients": total_patients
    }


@router.get("/users/{user_email}")
async def get_user_details(
    user_email: str,
    current_user: Dict = Depends(require_role("doctor"))
):
    """Get specific user details (doctor only)"""
    users_collection = get_users_collection()
    
    user = users_collection.find_one(
        {"email": user_email},
        {"password": 0, "_id": 0}
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
