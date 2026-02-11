from fastapi import FastAPI
from src.routers.user_router import router as user_router  # rutas de usuarios

app = FastAPI(title="CRM Restaurante")  # app FastAPI

# incluir routers
app.include_router(user_router, prefix="/users", tags=["Users"])


