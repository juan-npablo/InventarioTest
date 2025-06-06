from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from services import category_service
from core.security import require_admin, require_operator, require_viewer
from db.models.user import User

router = APIRouter(tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(require_operator)):
    return category_service.create_category(db, category, current_user.id)

@router.get("/", response_model=list[CategoryResponse])
def get_all(db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    return category_service.get_all_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse)
def get( category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    category = category_service.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
def update(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_operator)):
    category = category_service.update_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    category = category_service.delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}
