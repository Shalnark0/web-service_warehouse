from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from utils.security import hash_password, verify_password

def register_user(user, db: Session):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(user_login, db: Session):
    db_user = db.query(User).filter(User.username == user_login.username).first()
    if not db_user or not verify_password(user_login.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return db_user