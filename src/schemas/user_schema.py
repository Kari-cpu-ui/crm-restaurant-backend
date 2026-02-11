from pydantic import BaseModel                    # Validación

class UserCreate(BaseModel):                      # Crear usuario
    name: str
    email: str
    password: str

class UserRead(UserCreate):                       # Leer usuario
    id: int

    class Config:
        from_attributes = True                    # SQLAlchemy

