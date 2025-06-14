from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.auth import UserCreate, Token
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = auth_service.create_user(db, user)
    token = auth_service.generate_token(db_user.id)
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    auth_user = auth_service.authenticate_user(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth_service.generate_token(auth_user.id)
    return {"access_token": token}
