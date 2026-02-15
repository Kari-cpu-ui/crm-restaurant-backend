from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr

# Base ORM
Base = declarative_base()

# Modelo SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)  # rol como string normal


# Modelos Pydantic para validación
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    is_admin: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Config:
    from_attributes = True
