from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from db import get_db
from src.models.user_model import User
from auth import get_password_hash, verify_password, create_access_token

router = APIRouter()

# Esquemas Pydantic
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):
    try:
        email = data.get("email")
        name = data.get("name")
        password = data.get("password")

        if not email or not name or not password:
            raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        new_user = User(
            name=name,
            email=email,
            password=get_password_hash(password),
            is_admin=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Usuario registrado exitosamente", "user_id": new_user.id}

    except HTTPException as e:
        raise e
    except Exception as e:
        # Captura errores inesperados
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# Login seguro
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({
        "sub": user.email,
        "is_admin": user.is_admin
    })

    return {"access_token": token, 
            "token_type": "bearer",
            "is_admin": user.is_admin}
