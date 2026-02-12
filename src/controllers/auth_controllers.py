from fastapi import HTTPException
from db import get_conexion
from models.user_model import UserCreate, UserLogin
import db as Base
from auth import hash_password, verify_password, create_token


async def register(user: UserCreate):
    try:
        conn = await get_conexion()
        async with conn.cursor(Base.DictCursor) as cursor:
            hashed_pass = hash_password(user.password)
            await cursor.execute(
                "INSERT INTO users (name,email,password,role, is_active) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (
                    user.name,
                    user.email,
                    hashed_pass,
                    user.role,
                    user.is_active,
                ),
            )
            await conn.commit()
            new_id = cursor.lastrowid
            user = await ("SELECT * FROM 202509_shop.users WHERE id=%s", (new_id))
            return {"msg": "Usuario registrado correctamente", "item": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


async def login(user_login: UserLogin):
    try:
        conn = await get_conexion()
        async with conn.cursor(Base.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM 202509_shop.users WHERE mail=%s", (user_login.mail)
            )
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(
                    status_code=404, detail="Usuario o password incorrecto"
                )

            # verificar la contraseña
            if not verify_password(user_login.password, user["password"]):
                raise HTTPException(
                    status_code=404, detail="Usuario o password incorrecto"
                )
            # vamos crear el token con los datos y la funcion que hemos trabajado en security
            token_data = {"id": user["id"], "rol": user["rol"]}
            token = create_token(token_data)
            return {"msg": "Usuario logado correctamente", "token": token}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()