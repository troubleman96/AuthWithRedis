from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.auth import UserCreate, Token, RefreshTokenRequest,  TokenWithRefresh
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenWithRefresh)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = auth_service.create_user(db, user)
    access_token, refresh_token = auth_service.generate_tokens(db_user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/login", response_model=TokenWithRefresh)
def login(user: UserCreate, db: Session = Depends(get_db)):
    auth_user = auth_service.authenticate_user(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token, refresh_token = auth_service.generate_tokens(auth_user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh-token", response_model=Token)
def refresh_token(request: RefreshTokenRequest):
    new_access_token = auth_service.refresh_access_token(request.refresh_token)
    if not new_access_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return {"access_token": new_access_token}
