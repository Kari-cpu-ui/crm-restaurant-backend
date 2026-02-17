from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class PizzaOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str

    class Config:
        orm_mode = True

class MenuOut(BaseModel):
    menu_date: str
    title: Optional[str] = None
    pizzas: List[PizzaOut]

    class Config:
        orm_mode = True

# Para crear/recibir pizzas dentro de un menú
class PizzaInMenu(BaseModel):
    id: int  # id de la pizza existente
    # Opcional si quieres permitir precio/categoría personalizado
    # price: float
    # category: str

# Schema para crear un menú
class MenuCreate(BaseModel):
    menu_date: str  # o date si quieres convertir a datetime.date
    title: Optional[str] = None
    pizzas: List[PizzaInMenu]  # lista de pizzas que estarán en este menú

    class Config:
        orm_mode = True

class MenuResponse(BaseModel):
    id:int
    name: str
    menu_date: date
    description: str
    price: float
    category_id: int
    is_active: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True