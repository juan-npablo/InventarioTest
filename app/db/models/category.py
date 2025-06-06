from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    
    created_by = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="categories")
    
    products = relationship("Product", back_populates="category", cascade="all, delete")
