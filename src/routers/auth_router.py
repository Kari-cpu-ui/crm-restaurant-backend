from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from src.models.user_model import User
from auth import verify_password, create_access_token, get_password_hash

router = APIRouter(prefix="/users/auth", tags=["Auth"])

# ----------------------------
# Esquemas Pydantic
# ----------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

# ----------------------------
# Login
# ----------------------------
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({
        "sub": user.email,
        "is_admin": user.is_admin,
        "password": user.password
    })
    return {"access_token": token, "token_type": "bearer"}



# ----------------------------
# Registro
# ----------------------------
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    new_user = User(
        name=data.name,
        email=data.email,
        password=get_password_hash(data.password),
        is_admin=False  # usuarios nuevos no son admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado exitosamente", "user_id": new_user.id}
