from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    operador = "operador"
    visualizador = "visualizador"

class UserBase(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr
    role: UserRole = UserRole.visualizador

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):

    class Config:
        orm_mode = True
