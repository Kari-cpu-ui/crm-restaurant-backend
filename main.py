from fastapi import FastAPI # Franwork
from db import engine, SessionLocal
from src.models import user_model, table_model, reservation_model
from src.models.user_model import User
from src.routers.user_router import router as user_router  # import rutas de usuarios
from src.routers.auth_router import router as auth_router # import rutas para el login

from auth import hash_password # password

app = FastAPI(title="CRM Restaurante")  # Crear app FastAPI

@app.get("/")
def read_root():
    return {"menssage": "Servidor funcionando correctamente"}

user_model.Base.metadata.create_all(bind=engine)
table_model.Base.metadata.create_all(bind=engine)
reservation_model.Base.metadata.create_all(bind=engine) 

# incluir/conectar routers
app.include_router(user_router)
app.include_router(auth_router)


#  crear admin
def create_default_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin:
        new_admin = User(
            username="admin",
            email="admin@restaurant.com",
            password=hash_password("admin123"),
            is_admin=False
        )
        db.add(new_admin)
        db.commit()
    
    db.close()

