from sqlalchemy import Column, Integer, String    # Tipos columnas
from db import Base                               # Base común

class User(Base):                                 # Tabla users
    __tablename__ = "users"                       # Nombre tabla

    id = Column(Integer, primary_key=True)        # ID
    name = Column(String(100), nullable=False)    # Nombre
    email = Column(String(100), unique=True)      # Email
    password = Column(String(255), nullable=False)# Password

