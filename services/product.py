from sqlalchemy.orm import Session
from models.product import Product as ProductModel
from schemas.product import ProductCreate, ProductUpdate
from uuid import UUID

def create_product(product: ProductCreate, db: Session):
    new_product = ProductModel(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_products(db: Session):
    return db.query(ProductModel).all()

def get_product_by_id(product_id: UUID, db: Session):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def update_product(product: ProductUpdate, product_id: UUID, db: Session):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(product_id: UUID, db: Session):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
