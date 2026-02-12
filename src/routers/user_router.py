from fastapi import APIRouter, Depends             # Router y dependencias
from sqlalchemy.orm import Session                # Tipo Sesión DB
from db import SessionLocal                       # Creador de sesiones
from src.models.user_model import User                # Modelo (Object Relational Mapping)
from src.schemas.user_schema import UserCreate, UserRead  # Esquemas

router = APIRouter(  # Router independiente
    prefix="/users",                             
    tags=["Users"]                                
)

def get_db():            # Dependencia DB
    db = SessionLocal()   # Crear sesión
    try:
        yield db     # Entregar sesión
    finally:
        db.close()  # Cerrar sesión

@router.get("/", response_model=list[UserRead])  # GET users
def get_users(db: Session = Depends(get_db)): # Inyecta sesión
    return db.query(User).all() # SELECT * FROM users

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


