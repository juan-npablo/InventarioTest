from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    stock = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey("categories.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="products")
    creator = relationship("User", back_populates="products")
    movements = relationship("Movement", back_populates="product", cascade="all, delete")
