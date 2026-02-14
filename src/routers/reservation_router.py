from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from src.models.reservation_model import Reservation
from src.models.table_model import Table
from src.schemas.reservation_schema import ReservationCreate, ReservationRead

# Router independiente para reservas
router = APIRouter(
    prefix="/reservations",  # Todas las rutas empiezan con /reservations
    tags=["Reservations"]
)

# Dependencia para la sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Listar todas las reservas
@router.get("/", response_model=list[ReservationRead])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

# Crear nueva reserva
@router.post("/", response_model=ReservationRead)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == reservation.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    if reservation.guests > table.capacity:
        raise HTTPException(status_code=400, detail="Número de invitados excede la capacidad de la mesa")
    existing = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.date == reservation.date,
        Reservation.status == "active"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mesa ya reservada para esta fecha")

    db_reservation = Reservation(
        table_id=reservation.table_id,
        customer_name=reservation.customer_name,
        date=reservation.date,
        guests=reservation.guests
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# Cancelar reserva
@router.delete("/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    reservation.status = "cancelled"
    db.commit()
    return {"detail": "Reserva cancelada correctamente"}
