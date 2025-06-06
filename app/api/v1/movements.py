from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.schemas.movement import MovementCreate, MovementResponse
from services import movement_service
from core.security import require_admin, require_operator, require_viewer
from db.models.user import User

router = APIRouter(tags=["Movements"])

@router.post("/", response_model=MovementResponse)
def create(data: MovementCreate, db: Session = Depends(get_db), current_user: User = Depends(require_operator)):
    result = movement_service.create_movement(db, data, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    elif result == "Insufficient stock":
        raise HTTPException(status_code=400, detail="Insufficient stock for movement")
    return result

@router.get("/", response_model=list[MovementResponse])
def get_all(db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    return movement_service.get_all_movements(db)

@router.get("/{movement_id}", response_model=MovementResponse)
def get_by_id(movement_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    movement = movement_service.get_movement_by_id(db, movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement

@router.get("/product/{product_id}", response_model=list[MovementResponse])
def get_by_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_viewer)):
    return movement_service.get_movements_by_product(db, product_id)

@router.delete("/{movement_id}")
def delete(movement_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    movement = movement_service.delete_movement(db, movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return {"message": "Movement deleted and stock adjusted"}
