from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from uuid import UUID
from utils.security import hash_password

def create_user(user: UserCreate, db: Session):
    hashed_pw = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(user_id: UUID, db: Session):
    return db.query(User).filter(User.id == user_id).first()

def update_user(user: UserCreate, user_id: UUID, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = hash_password(user.password)
        db_user.role = user.role
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(user_id: UUID, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()