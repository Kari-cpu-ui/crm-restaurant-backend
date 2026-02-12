from sqlalchemy import Column, Integer, String, Boolean    # Tipos columnas
from db import Base                               # Base común ORM

class Rol(str):
    cliente = "cliente"
    administrador = "administrador"

class User:                                 # Modelo users
    __tablename__ = "users"                       # Nombre tabla en MySQL
 
    id = Column(Integer, primary_key=True)        # ID 
    name = Column(String(100), nullable=False)    # Nombre obligatorio
    email = Column(String(100), unique=True)      # Email único
    password = Column(String(255), nullable=False)# Password obligatorio
    role = Column(String(10), default=Rol.cliente)
    is_active = Column(Boolean, default=True)
    
class UserCreate:
    name: str
    email: str
    password: str
    role: str
    is_active: bool
    
class UserLogin:
    mail: str
    password: str

