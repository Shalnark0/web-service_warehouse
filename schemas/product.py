from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: UUID

    class Config:
        orm_mode = True
