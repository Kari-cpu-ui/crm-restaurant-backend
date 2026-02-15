from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext


# Configuración JWT

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Configuración Password Hashing


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Funciones de Password


def get_password_hash(password: str) -> str:
    """
    Recibe contraseña en texto plano y devuelve hash bcrypt.
    Se trunca a 72 bytes por limitación interna de bcrypt.
    """
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica contraseña en texto plano contra hash almacenado.
    """
    return pwd_context.verify(plain_password[:72], hashed_password)


# JWT


def create_access_token(email: str, is_admin: bool = False) -> str:
    """
    Genera un token JWT seguro, solo con información mínima necesaria:
    - sub: email del usuario
    - is_admin: rol de administrador
    - exp: fecha de expiración
    """
    to_encode = {
        "sub": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
