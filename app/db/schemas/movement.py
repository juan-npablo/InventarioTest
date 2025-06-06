from pydantic import BaseModel
from enum import Enum

class MovementType(str, Enum):
    entrada = "entrada"
    salida = "salida"

class MovementBase(BaseModel):
    product_id: int
    quantity: int
    type: MovementType

class MovementCreate(MovementBase):
    pass

class MovementResponse(MovementBase):
    id: int

    class Config:
        orm_mode = True
