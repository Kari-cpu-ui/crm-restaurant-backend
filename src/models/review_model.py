from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    rating = Column(Integer, nullable=False)                  # Puntuación de 1 a 5
    comment = Column(String(500), nullable=False)              # Comentario obligatorio
    created_at = Column(DateTime, default=datetime.utcnow)    # Fecha de creación

    reservation = relationship("Reservation")                 # Relación ORM con reserva
