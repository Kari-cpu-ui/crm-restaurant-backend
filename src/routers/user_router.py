from fastapi import APIRouter, Depends             # Router
from sqlalchemy.orm import Session                # Sesión DB
from db import SessionLocal                       # DB
from src.models.user_model import User                # Modelo
from src.schemas.user_schema import UserCreate, UserRead  # Esquemas

router = APIRouter(
    prefix="/users",                              # /users
    tags=["Users"]                                # Docs
)

def get_db():                                     # Abrir DB
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserRead])  # GET users
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/", response_model=UserRead)       # POST users
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(                               # Crear user
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)                               # Añadir
    db.commit()                                   # Guardar
    db.refresh(db_user)                           # Refrescar
    return db_user


