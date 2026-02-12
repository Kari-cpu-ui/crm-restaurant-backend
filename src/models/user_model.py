from sqlalchemy import Column, Integer, String    # Tipos columnas
from db import Base                               # Base común ORM 

class User(Base):                                 # Modelo users
    __tablename__ = "users"                       # Nombre tabla en MySQL
 
    id = Column(Integer, primary_key=True)        # ID 
    name = Column(String(100), nullable=False)    # Nombre obligatorio
    email = Column(String(100), unique=True)      # Email único
    password = Column(String(255), nullable=False)# Password obligatorio

