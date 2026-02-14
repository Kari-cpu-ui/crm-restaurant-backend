from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.user_model import User # Ajusta según tu estructura real

# Conexión a la BBDD
DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_O0d61P4Z-szU59jTuhV@mysql-2ca3943e-backendproject2026.i.aivencloud.com:12021/defaultdb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

# Mostrar todos los usuarios
usuarios = db.query(User).all()
for u in usuarios:
    print(u.id, u.name, u.email, u.is_admin)

db.close()
