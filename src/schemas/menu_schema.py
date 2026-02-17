from pydantic import BaseModel


class MenuBase(BaseModel):
    date: str
    first_course: str
    second_course: str
    dessert: str
    price: float


class MenuCreate(MenuBase):
    pass


class MenuResponse(MenuBase):
    id: int

    class Config:
        from_attributes = True
