from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from db.base_class import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    operador = "operador"
    visualizador = "visualizador"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.visualizador)

    # Relaciones
    products = relationship("Product", back_populates="creator", cascade="all, delete")
    categories = relationship("Category", back_populates="creator", cascade="all, delete")
    movements = relationship("Movement", back_populates="creator", cascade="all, delete")
