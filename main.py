"""
FastAPI RBAC Application - Main Entry Point
Modular Architecture with JWT Authentication and MongoDB
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, users, doctors, health

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Role-Based Access Control (RBAC) system with JWT authentication and MongoDB"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(doctors.router)
app.include_router(health.router)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    connect_to_mongo()
    print(f"✓ {settings.APP_NAME} started")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    close_mongo_connection()
    print(f"✓ {settings.APP_NAME} stopped")


# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "RBAC API is running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

