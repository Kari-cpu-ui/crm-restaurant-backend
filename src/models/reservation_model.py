from sqlalchemy import Column, Integer, String, Date, ForeignKey # Tipos de columnas y FW
from sqlalchemy.orm import relationship # Relación ORM
from db import Base # Base Común 
from src.models.table_model import Table # Importar modelo table

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)  # FK a mesa
    customer_name = Column(Integer, ForeignKey("users.id"), nullable=False)   # FK a usuario
    date = Column(Date, nullable=False)                                 # Fecha de reserva
    guests = Column(Integer, nullable=False)                            # Cantidad de personas
    status = Column(String(20), default="active") 

    table = relationship("Table")                                    # Relación ORM con mesa
    user = relationship("User")