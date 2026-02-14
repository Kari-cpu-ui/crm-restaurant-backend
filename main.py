from fastapi import FastAPI  # Framework
from db import engine, SessionLocal
from src.models import user_model, table_model, reservation_model
from src.models.user_model import User, Rol
from src.routers.user_router import router as user_router
from src.routers.auth_router import router as auth_router
from src.routers.table_router import router as table_router
from src.routers.reservation_router import router as reservation_router
from auth import hash_password  # password


app = FastAPI(title="CRM Restaurante")

@app.get("/")
def read_root():
    return {"message": "Servidor funcionando correctamente"}

# Conectar routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/users/auth", tags=["Auth"])
app.include_router(table_router)           
app.include_router(reservation_router)    
