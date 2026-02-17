from sqlalchemy import Column, Integer, String, Float, Date
from db import Base


class Menu(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_date = Column(Date, nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer)
    is_active = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=True)
