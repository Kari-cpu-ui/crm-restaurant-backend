from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from src.models.review_model import Review
from src.models.reservation_model import Reservation
from src.schemas.review_schema import ReviewCreate, ReviewRead

# Router independiente para reseñas
router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

# Dependencia para la sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Listar todas las reseñas
@router.get("/", response_model=list[ReviewRead])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

# Obtener reseña por ID
@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    return review

# Crear nueva reseña
@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == review.reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    existing = db.query(Review).filter(Review.reservation_id == review.reservation_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una reseña para esta reserva")

    db_review = Review(
        reservation_id=review.reservation_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
