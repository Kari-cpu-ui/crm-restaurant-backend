from pydantic import BaseModel
from typing import Optional

# Schema para crear una mesa
class TableCreate(BaseModel):
    name: str
    capacity: int

# Schema para leer una mesa (lo mismo, pero puedes añadir id)
class TableRead(BaseModel):
    id: int
    name: str
    capacity: int

    class Config:
        orm_mode = True   # Muy importante para que funcione con SQLAlchemy

# Schema para actualizar una mesa (campos opcionales)
class TableUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None