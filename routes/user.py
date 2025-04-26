from uuid import UUID
from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserOut, UserRole
from services.user import create_user, get_users, get_user_by_id, update_user, delete_user
from sqlalchemy.orm import Session
from database.database import get_db

router = APIRouter()

@router.post("/", response_model=UserOut)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.get("/", response_model=list[UserOut])
def read(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserOut)
def read_by_id(user_id: UUID, db: Session = Depends(get_db)):
    return get_user_by_id(user_id, db)

@router.put("/{user_id}", response_model=UserOut)
def update(user: UserCreate, user_id: UUID, db: Session = Depends(get_db)):
    return update_user(user, user_id, db)

@router.delete("/{user_id}")
def delete(user_id: UUID, db: Session = Depends(get_db)):
    delete_user(user_id, db)
    return {"message": "User deleted successfully!"}