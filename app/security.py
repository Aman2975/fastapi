"""
Security utilities for JWT and password hashing
"""
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer
from app.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# HTTP Bearer security
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash password using Argon2"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_access_token(email: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": email,
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(credentials = Depends(security)) -> Dict:
    """Get current authenticated user from token"""
    token = credentials.credentials
    return verify_token(token)


def require_role(required_role: str):
    """Dependency to check user role"""
    async def role_checker(current_user: Dict = Depends(get_current_user)) -> Dict:
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This endpoint requires '{required_role}' role"
            )
        return current_user
    return role_checker
