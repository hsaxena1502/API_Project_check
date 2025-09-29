"""Security utilities for the API."""
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from src.utils.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    """Generate a hashed password.
    
    Args:
        password: The plain text password to hash.
        
    Returns:
        The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject of the token (usually user email or ID)
        expires_delta: Optional time delta for token expiration
        
    Returns:
        The encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt
