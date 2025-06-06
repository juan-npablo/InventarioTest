from sqlalchemy.orm import Session
from db.models.category import Category
from db.schemas.category import CategoryCreate, CategoryUpdate

def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    category = Category(
        name=category_data.name,
        created_by=user_id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_all_categories(db: Session):
    return db.query(Category).all()

def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = get_category_by_id(db, category_id)
    if not category:
        return None
    for attr, value in data.model_dump().items():
        setattr(category, attr, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category
