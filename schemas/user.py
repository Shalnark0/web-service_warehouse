from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID

    class Config:
        orm_mode = True
