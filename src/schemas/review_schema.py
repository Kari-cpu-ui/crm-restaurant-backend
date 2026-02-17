from pydantic import BaseModel, Field
from datetime import datetime


# Schema para crear una reseña
class ReviewCreate(BaseModel):
    reservation_code: str                            # Código de reserva (4 dígitos)
    rating: int = Field(..., ge=1, le=5)             # Puntuación de 1 a 5
    comment: str                                     # Comentario obligatorio


# Schema para devolver información de una reseña
class ReviewRead(ReviewCreate):
    id: int                                          # ID generado automáticamente
    created_at: datetime                             # Fecha de creación

    class Config:
        from_attributes = True                       # Permite convertir desde el modelo ORM
