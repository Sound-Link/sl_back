# user_router.py
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from sqlalchemy.orm import Session
from . import user_crud, user_schema
import models

router = APIRouter()

@router.post("/user_create/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.get("/user_all/", response_model=user_schema.UserList)
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return {"users": users}