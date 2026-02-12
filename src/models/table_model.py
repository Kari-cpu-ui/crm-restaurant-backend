from sqlalchemy import Column, Integer, String # Tipos de column para SQLAlchemy 
from db import Base # Base común para modelos ORM


class Table(Base):  #Modelo table(Mesa)
    __tablename__ = "tables" # Nombre de la tabla en BD
   

    id = Column(Integer, primary_key=True) # ID autoincremental de la mesa 
    number = Column(Integer, nullable=False, unique=True) # Número de mesa (único)
    name = Column(String(100), nullable=True)  # Nombre de la mesa, opcional (ej. "VIP")
    capacity = Column(Integer, nullable=False) # Cantidad de personas que pueden sentarse