from sqlalchemy import create_engine  # Crea la conexión a BBDD
from sqlalchemy.ext.declarative import declarative_base  # Base para modelos (ORM)
from sqlalchemy.orm import Session, sessionmaker  # Creador de sesiones
import os  # Acceso a variables de entorno
from dotenv import load_dotenv  # Cargar variables desde .env

load_dotenv()  # carga el archivo .env en memoria 

# Construcción de la URL de conexión MySQL desde variables de entorno
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Motor de conexión de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para ver queries en consola

# Creador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()  # Clase Base para todos los modelos 

# Función get_db para usar con Depends
def get_db():
    db: Session = SessionLocal()  # Crear sesión
    try:
        yield db  # yield la hace usable como dependencia
    finally:
        db.close()  # Cerrar al terminar
