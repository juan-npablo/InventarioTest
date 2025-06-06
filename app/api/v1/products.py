from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from services import product_service
from core.security import require_admin, require_operator, require_viewer
from db.models.user import User

router = APIRouter(tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(require_operator)):
    return product_service.create_product(db, product, current_user.id)

@router.get("/", response_model=list[ProductResponse])
def get_all(db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    return product_service.get_all_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_operator)):
    product = product_service.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    product = product_service.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
