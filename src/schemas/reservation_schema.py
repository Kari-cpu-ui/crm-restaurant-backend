from pydantic import BaseModel
from datetime import date

# Schema para crear una reserva
class ReservationCreate(BaseModel):
    table_id: int         # ID de la mesa
    customer_name: str    # Nombre del cliente
    date: date            # Fecha de reserva
    guests: int           # Cantidad de personas

# Schema para devolver información de una reserva
class ReservationRead(ReservationCreate):
    id: int               # ID generado automáticamente
    status: str           # Estado: "active" o "cancelled"

    class Config:
         from_attributes = True  # Permite convertir desde el modelo ORM
