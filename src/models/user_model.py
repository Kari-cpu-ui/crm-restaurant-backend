from sqlalchemy import Column, Integer, String, Boolean    # Tipos columnas
from db import Base                               # Base común ORM

class Rol(str):
    cliente = "cliente"
    administrador = "administrador"

class User(Base):                                 # Modelo users
    __tablename__ = "users"                       # Nombre tabla en MySQL
 
    id = Column(Integer, primary_key=True)        # ID 
    name = Column(String(100), nullable=False)    # Nombre obligatorio
    email = Column(String(100), unique=True)      # Email único
    password = Column(String(255), nullable=False)# Password obligatorio
    role = Column(String(10), default=Rol.cliente)
    is_active = Column(Boolean, default=True)
    
# Comentadas para evitar que SQLAlchemy intente mapearlas como modelos ORM.
# Si se desean usar como esquemas Pydantic, moverlas a `src/schemas/user_schema.py`.
#
# class UserCreate(Base):
#     name: str
#     email: str
#     password: str
#     role: str
#     is_active: bool
#
# class UserLogin(Base):
#     mail: str
#     password: str


