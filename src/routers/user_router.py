from fastapi import APIRouter, Depends             # Router y dependencias
from sqlalchemy.orm import Session                # Tipo Sesión DB
from db import SessionLocal, get_db                       # Creador de sesiones
from src.models.user_model import User                # Modelo (Object Relational Mapping)
from src.schemas.user_schema import UserCreate, UserRead  # Esquemas
from pydantic import BaseModel

# --- Agregado esto para evitar el error de UserResponse ---
class UserResponse(BaseModel):             #  Defino UserResponse para la salida GET users
    id: int
    name: str
    email: str
    is_admin: bool
 
    class Config:                          #  Configuración para que funcione con SQLAlchemy
        from_attributes = True

router = APIRouter()

def get_db():            # Dependencia DB
    db = SessionLocal()   # Crear sesión
    try:
        yield db     # Entregar sesión
    finally:
        db.close()  # Cerrar sesión

# @router.get("/", response_model=list[UserRead])  # GET users
# def get_users(db: Session = Depends(get_db)): # Inyecta sesión
#     return db.query(User).all() # SELECT * FROM users

@router.get("/", response_model=list[UserResponse])  # GET users
def get_users(db: Session = Depends(get_db)): # Inyecta sesión
    users = db.query(User).all()
    return users # SELECT * FROM users

@router.post("/", response_model=UserRead)       # POST users
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(                               # Crear objeto OMR
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)    # Preparar INSERT
    db.commit()        # Ejecutar INSERT
    db.refresh(db_user) # Recargar dede DB
    return db_user     # Retornar usuario                      


