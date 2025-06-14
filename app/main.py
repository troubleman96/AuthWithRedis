from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from app.api import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
