from sqlalchemy import create_engine # Crea la conexión a BBDD
from sqlalchemy.ext.declarative import declarative_base # Base para modelos (Object Relational Mapping "ORM")
from sqlalchemy.orm import sessionmaker # Creador de modelos 
import os  # Acceso a variables de entorno
from dotenv import load_dotenv # Cargar variables desde .env

load_dotenv()  # carga el archivo .env en memoria 

# Construcción la URL de conexión MySQL
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Motor de conección de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para ver queries en consola

# Sesiones para consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # No guarda automáticamente 

# Base para modelos
Base = declarative_base()
                       # Clase Base para todos los modelos 


def get_db():
    """Yield a SQLAlchemy Session and ensure it's closed after use.

    This is used as a FastAPI dependency in routers (Depends(get_db)).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



