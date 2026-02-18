from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from db import SessionLocal
from typing import List
from src.models.menu_model import Menu
from src.schemas.menu_schema import MenuCreate, MenuUpdate, MenuResponse


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
def get_menu_by_id(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


# Crear menú
@router.post("/", response_model=MenuResponse, status_code=201)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    date_obj = None
    if menu.menu_date:
        try:
            date_obj = datetime.strptime(menu.menu_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido")

    db_menu = Menu(
        name=menu.name,
        menu_date=date_obj,
        description=menu.description,
        price=menu.price,
        category_id=1,
        is_active=1,
        image_url=menu.image_url if menu.image_url else None
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


# Actualizar menú
@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    db_menu.name = menu.name
    db_menu.description = menu.description
    db_menu.price = menu.price
    db_menu.image_url = menu.image_url
    if menu.menu_date:
        try:
            db_menu.menu_date = datetime.strptime(menu.menu_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido")
    db.commit()
    db.refresh(db_menu)
    return db_menu


# Eliminar menú
@router.delete("/{menu_id}", status_code=200)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    db.delete(db_menu)
    db.commit()
    return {"message": "Menú eliminado correctamente"}
