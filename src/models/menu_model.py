from sqlalchemy import Column, Integer, String, Float
from db import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10), unique=True, nullable=False)        # Formato "YYYY-MM-DD"
    first_course = Column(String(200), nullable=False)            # Primer plato (antipasti)
    second_course = Column(String(200), nullable=False)           # Segundo plato (pizza)
    dessert = Column(String(200), nullable=False)                 # Postre
    price = Column(Float, nullable=False)                         # Precio del menú
