from sqlalchemy.orm import Session
from app.db import models
from app.schemas.auth import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
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
