from sqlalchemy.orm import Session
from app.db import models
from app.schemas.auth import UserCreate
from app.core.security import hash_password, verify_password, create_access_token, decode_token, create_refresh_token
from app.core.config import settings
from datetime import timedelta
from app.redis.client import r

def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": str(user_id)}, expires_delta=access_token_expires)

    # Save session in Redis
    r.setex(f"user_session:{user_id}", settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, token)
    return token

def generate_tokens(user_id: int):
    # Access Token (short-lived)
    access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user_id)}, expires_delta=access_expires)

    # Refresh Token (long-lived)
    refresh_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(data={"sub": str(user_id)}, expires_delta=refresh_expires)

    # Save refresh token in Redis
    r.setex(f"refresh_token:{user_id}", refresh_expires.seconds + refresh_expires.days * 86400, refresh_token)

    return access_token, refresh_token

def refresh_access_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload:
        return None

    user_id = payload.get("sub")
    stored_token = r.get(f"refresh_token:{user_id}")
    if stored_token != refresh_token:
        return None

    # Re-issue new access token
    access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_id}, expires_delta=access_expires)
    return access_token

def generate_tokens(user_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user_id)}, expires_delta=access_token_expires)
    
    # For example, refresh token expires in 7 days
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_access_token(data={"sub": str(user_id)}, expires_delta=refresh_token_expires)
    
    # Store refresh token in Redis with expiry
    r.setex(f"refresh_token:{user_id}", int(refresh_token_expires.total_seconds()), refresh_token)
    
    return access_token, refresh_token