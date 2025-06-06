from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base
import enum

class MovementType(str, enum.Enum):
    entrada = "entrada"
    salida = "salida"

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer, nullable=False)
    type = Column(Enum(MovementType), nullable=False)

    product = relationship("Product", back_populates="movements")
    creator = relationship("User", back_populates="movements")
