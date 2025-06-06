from sqlalchemy.orm import Session
from db.models.product import Product
from db.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, product_data: ProductCreate, user_id: int):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        category_id=product_data.category_id,
        stock=product_data.stock,
        created_by=user_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    for attr, value in data.model_dump(exclude_unset=True).items():
        setattr(product, attr, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product
