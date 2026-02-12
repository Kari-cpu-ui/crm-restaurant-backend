from fastapi import FastAPI # Franwork
from db import engine
from src.models import user_model, table_model, reservation_model, user_model
from src.routers.user_router import router as user_router  # import rutas de usuarios

app = FastAPI(title="CRM Restaurante")  # Crear app FastAPI

@app.get("/")
def read_root():
    return {"menssage": "Servidor funcionando correctamente"}

user_model.Base.metadata.create_all(bind=engine)
table_model.Base.metadata.create_all(bind=engine)
reservation_model.Base.metadata.create_all(bind=engine) 

# incluir/conectar routers
app.include_router(user_router, prefix="/users", tags=["Users"])

