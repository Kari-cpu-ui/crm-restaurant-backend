import random
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from db import SessionLocal
from src.models.reservation_model import Reservation
from src.models.review_model import Review
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

def generate_reservation_code(db: Session) -> str:
    """Genera un código único de 4 dígitos numéricos."""
    while True:
        code = f"{random.randint(0, 9999):04d}"
        existing = db.query(Reservation).filter(Reservation.reservation_code == code).first()
        if not existing:
            return code

# Crear nueva reserva
MAX_PERSONS_PER_SLOT = 10 # Límite de personas por franja horaria

@router.post("/", response_model=ReservationRead)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):

    # No permitir fechas pasadas
    if reservation.date < date.today():
        raise HTTPException(
            status_code=400,
            detail="No puedes hacer una reserva en una fecha pasada."
        )
    # Sumar cuantos invitados ya hay en ese día y hora
    total_guests = db.query(func.coalesce(func.sum(Reservation.guests), 0)).filter(
        Reservation.date == reservation.date,
        Reservation.time == reservation.time
    ).scalar()
    if total_guests + reservation.guests > MAX_PERSONS_PER_SLOT:
        raise HTTPException(status_code=400, detail="No hay suficiente disponibilidad para esa franja horaria.")
    
    # Crear la reserva
    code = generate_reservation_code(db)
    db_reservation = Reservation(
        reservation_code=code,
        time=reservation.time,
        customer_name=reservation.customer_name,
        date=reservation.date,
        guests=reservation.guests
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# Obtener reservas por usuario
@router.get("/user/{user_id}", response_model=list[ReservationRead])
def get_reservations_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.customer_name == user_id).all()

# Eliminar reserva
@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Eliminar reseñas asociadas antes de eliminar la reserva (FK constraint)
    db.query(Review).filter(Review.reservation_code == reservation.reservation_code).delete()
    db.delete(reservation)
    db.commit()
    return {"message": "Reserva cancelada correctamente"}
