from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.firestore import get_db
from app.schema.models import User, UserCreate
from app.core.security import get_password_hash, verify_password

router = APIRouter()

@router.get('/users/', response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# HUMAN ASSISTANCE NEEDED
# This function needs additional error handling and input validation
@router.post('/users/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users/{user_id}', response_model=User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# HUMAN ASSISTANCE NEEDED
# This function needs additional error handling and input validation
@router.put('/users/{user_id}', response_model=User)
def update_user(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.email = user.email
    db_user.full_name = user.full_name
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user