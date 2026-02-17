from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from db import SessionLocal
from typing import List
from src.models.menu_model import Menu
from src.schemas.menu_schema import MenuCreate, MenuResponse, MenuOut


router = APIRouter(
    prefix="/menus",
    tags=["Menus"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint para obtener menú por fecha
@router.get("/{menu_date}", response_model=MenuOut)
def get_menu(menu_date: str, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.date == menu_date).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")

    # Convertimos a formato con pizzas como lista
    pizzas = [
        {"name": menu.name, "category": "menu.description", "price": menu.price},
    ]
    return {"menu_date": menu.date, "pizzas": pizzas}


# Listar todos los menús
@router.get("/", response_model=list[MenuResponse])
def get_menus(db: Session = Depends(get_db)):
    return db.query(Menu).all()


# Obtener menú por fecha
@router.get("/date/{menu_date}", response_model=MenuResponse)
def get_menu_by_date(menu_date: str, db: Session = Depends(get_db)):

    try:
        date_obj = datetime.strptime(menu_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    menu = db.query(Menu).filter(Menu.menu_date == date_obj).first()

    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado para esta fecha")

    return menu



# Obtener menú por ID
@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    return menu


# Crear menú
@router.post("/", response_model=MenuResponse)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    existing = db.query(Menu).filter(Menu.date == menu.date).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un menú para esta fecha")
    db_menu = Menu(
        name=menu.name,
        menu_date=menu.menu_date,
        description=menu.description,
        price=menu.price,
        category_id=menu.category_id,
        is_active=menu.is_active,
        image_url=menu.image_url
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


# Actualizar menú
@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: int, menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    db_menu.name = menu.name
    db_menu.menu_date = menu.menu_date
    db_menu.description = menu.description
    db_menu.price = menu.price
    db_menu.category_id = menu.category_id
    db_menu.is_active = menu.is_active
    db_menu.image_url = menu.image_url
    db.commit()
    db.refresh(db_menu)
    return db_menu


# Eliminar menú
@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    db.delete(db_menu)
    db.commit()
    return {"message": "Menú eliminado correctamente"}
