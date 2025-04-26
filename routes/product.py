from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database.database import get_db
from dependencies.auth import get_current_user
from models.user import User
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from schemas.user import UserRole
from services.product import create_product, get_products, get_product_by_id, update_product, delete_product
from uuid import UUID
from typing import Annotated

router = APIRouter()

@router.post("/", response_model=ProductOut)
def create(product: ProductCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.role not in [UserRole.manager, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create products",
        )
    return create_product(product, db)

@router.get("/", response_model=list[ProductOut])
def read(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def read_by_id(product_id: UUID, db: Session = Depends(get_db)):
    return get_product_by_id(product_id, db)

@router.put("/{product_id}", response_model=ProductOut)
def update(product_id: UUID, product: ProductUpdate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.role not in [UserRole.manager, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update products",
        )
    return update_product(product, product_id, db)

@router.delete("/{product_id}")
def delete(product_id: UUID, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.role not in [UserRole.manager, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete products",
        )
    delete_product(product_id, db)
    return {"message": "Deleted"}