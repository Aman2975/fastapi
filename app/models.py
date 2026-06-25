"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """User registration model"""
    email: str
    password: str
    full_name: str
    role: str  # "doctor" or "user"
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        if len(v) > 500:
            raise ValueError('Password must be less than 500 characters')
        return v
    
    @validator('role')
    def validate_role(cls, v):
        if v not in ["doctor", "user"]:
            raise ValueError('Role must be "doctor" or "user"')
        return v


class UserLogin(BaseModel):
    """User login model"""
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) > 500:
            raise ValueError('Password must be less than 500 characters')
        return v


class TokenResponse(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str
    role: str


class UserResponse(BaseModel):
    """User response model"""
    email: str
    full_name: str
    role: str
    created_at: str


class UserProfile(BaseModel):
    """User profile model"""
    email: str
    full_name: str
    role: str
    created_at: str
    is_active: bool
