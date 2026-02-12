from db import SessionLocal
from src.models.user_model import User, Rol
from src.routers.auth_router import hash_password


def create_default_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()

        if not admin:
            new_admin = User(
                username="admin",
                email="admin@restaurant.com",
                hashed_password=hash_password("admin123"),
                role=Rol.administrador
            )
            db.add(new_admin)
            db.commit()
            print("Administrador creado correctamente")
        else:
            print("Administrador ya existe")

    finally:
        db.close()
