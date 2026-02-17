from sqlalchemy import Column, Integer, String, Date, ForeignKey # Tipos de columnas y FW
from sqlalchemy.orm import relationship # Relación ORM
from db import Base # Base Común 

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    reservation_code = Column(String(4), unique=True, nullable=False)   # Código único de 4 dígitos
    time = Column(String(5), nullable=False)                            # Hora de reserva (ej: "14:00")
    customer_name = Column(Integer, ForeignKey("users.id"), nullable=False)   # FK a usuario
    date = Column(Date, nullable=False)                                 # Fecha de reserva
    guests = Column(Integer, nullable=False)                            # Cantidad de personas
    status = Column(String(20), default="active") 

    user = relationship("User")