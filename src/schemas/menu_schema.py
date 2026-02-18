from datetime import date
from pydantic import BaseModel
from typing import Optional


class MenuCreate(BaseModel):
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    menu_date: Optional[str] = None


class MenuUpdate(BaseModel):
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    menu_date: Optional[str] = None


class MenuResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    is_active: int
    image_url: Optional[str] = None
    menu_date: Optional[date] = None

    class Config:
        from_attributes = True