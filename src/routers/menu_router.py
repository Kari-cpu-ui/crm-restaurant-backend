from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from src.models.menu_model import Menu
from src.schemas.menu_schema import MenuCreate, MenuResponse

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
@router.get("/date/{date}", response_model=MenuResponse)
def get_menu_by_date(date: str, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.date == date).first()
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
        date=menu.date,
        first_course=menu.first_course,
        second_course=menu.second_course,
        dessert=menu.dessert,
        price=menu.price
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
    db_menu.date = menu.date
    db_menu.first_course = menu.first_course
    db_menu.second_course = menu.second_course
    db_menu.dessert = menu.dessert
    db_menu.price = menu.price
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
