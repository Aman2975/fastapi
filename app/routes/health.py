"""
Health check routes
"""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Public health check endpoint"""
    return {
        "status": "healthy",
        "service": "RBAC API with JWT & MongoDB"
    }
