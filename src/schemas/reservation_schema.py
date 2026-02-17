from pydantic import BaseModel
from datetime import date

# Schema para crear una reserva
class ReservationCreate(BaseModel):
    time: str             # Hora de reserva (ej: "14:00")
    customer_name: str    # Nombre del cliente
    date: date            # Fecha de reserva
    guests: int           # Cantidad de personas

    class Config:
        orm_mode = True

# Schema para devolver información de una reserva
class ReservationRead(ReservationCreate):
    id: int                    # ID generado automáticamente
    reservation_code: str      # Código único de 4 dígitos
    status: str                # Estado: "active" o "cancelled"

    class Config:
        orm_mode = True  # Permite convertir desde el modelo ORM
