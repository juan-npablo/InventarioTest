from sqlalchemy.orm import Session
from db.models.movement import Movement, MovementType
from db.models.product import Product
from db.schemas.movement import MovementCreate

def create_movement(db: Session, data: MovementCreate, user_id: int):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        return None
    
    if ((data.type == MovementType.salida) and (product.stock < data.quantity)):
        return "Stock insuficiente para la salida"

    # Ajustar el stock
    if data.type == MovementType.entrada:
        product.stock += data.quantity
    else:
        product.stock -= data.quantity

    movement = Movement(
        product_id=data.product_id,
        quantity=data.quantity,
        type=data.type,
        created_by=user_id
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement

def get_movements_by_product(db: Session, product_id: int):
    return db.query(Movement).filter(Movement.product_id == product_id).all()

def get_all_movements(db: Session):
    return db.query(Movement).all()

def get_movement_by_id(db: Session, movement_id: int) -> Movement | None:
    return db.query(Movement).filter(Movement.id == movement_id).first()

#No se elimina el movimiento directamente ya que afectaría el 
#historial de movimintos de los productos
def delete_movement(db: Session, movement_id: int):
    movement = get_movement_by_id(db, movement_id)
    if not movement:
        return None

    # Revertir stock
    product = movement.product
    if movement.type == MovementType.entrada:
        product.stock -= movement.quantity
    else:
        product.stock += movement.quantity

    db.delete(movement)
    db.commit()
    return movement
