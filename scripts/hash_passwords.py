from db import SessionLocal
from src.models.user_model import User
from auth import get_password_hash


def is_bcrypt_hash(password: str) -> bool:
    """
    Verifica si la contraseña ya parece ser un hash bcrypt válido.
    """
    if not password:
        return False

    return password.startswith(("$2a$", "$2b$", "$2y$")) and len(password) >= 60


def hash_plaintext_passwords():
    db = SessionLocal()

    try:
        users = db.query(User).all()
        updated_count = 0

        for user in users:
            # Saltar si no hay password
            if not user.password:
                continue

            # Solo hashear si NO es ya un hash bcrypt
            if not is_bcrypt_hash(user.password):
                user.password = get_password_hash(user.password)
                db.add(user)
                updated_count += 1

        db.commit()
        print(f"✔ {updated_count} contraseñas hasheadas correctamente.")

    except Exception as e:
        db.rollback()
        print("❌ Error durante el proceso:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    hash_plaintext_passwords()
