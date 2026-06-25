"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://root:Kachura2003@100.64.200.118:27017/mydb?authSource=admin"
    DATABASE_NAME: str = "mydb"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App Configuration
    APP_NAME: str = "RBAC System with JWT & MongoDB"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
