import fastapi
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # para CORS
from db import engine, SessionLocal
# Import de módulos propios
from src.models import user_model, table_model, reservation_model, review_model
from src.models.user_model import User
from src.models import menu_model
from src.models.menu_model import Menu
from src.routers.user_router import router as user_router
from src.routers.auth_router import router as auth_router
from src.routers.table_router import router as table_router
from src.routers.reservation_router import router as reservation_router
from src.routers.review_router import router as review_router
from src.routers.menu_router import router as menu_router
from src.schemas.menu_schema import MenuCreate, MenuResponse, MenuOut
from auth import get_password_hash

# Inicializar FastAPI
app = FastAPI(title="CRM Restaurante")

# Configurar CORS
origins = [
    "http://localhost:4200",  # Angular
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite todas las IPs y dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz de prueba
@app.get("/")
def read_root():
    return {"message": "Servidor funcionando correctamente"}

# Crear tablas si no existen
user_model.Base.metadata.create_all(bind=engine)
table_model.Base.metadata.create_all(bind=engine)
reservation_model.Base.metadata.create_all(bind=engine)
review_model.Base.metadata.create_all(bind=engine)
menu_model.Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/users/auth", tags=["Auth"])
app.include_router(table_router)
app.include_router(reservation_router)
app.include_router(review_router)
app.include_router(menu_router)

# Crear admin por defecto
def create_default_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.name == "admin").first()
    
    if not admin:
        new_admin = User(
            name="admin",
            email="admin@restaurant.com",
            password=get_password_hash("admin123"),
            is_admin=False
        )
        db.add(new_admin)
        db.commit()
    
    db.close()

# Ejecutar creación del admin al iniciar
create_default_admin()


# Insertar menús semilla si la tabla está vacía
def seed_menus():
    db = SessionLocal()
    count = db.query(Menu).count()
    if count == 0:
        menus = [
            {"date": "2026-02-17", "first_course": "Antipasti de bruschetta clásica", "second_course": "Pizza Margherita", "dessert": "Tiramisú", "price": 15.00},
            {"date": "2026-02-18", "first_course": "Antipasti de carpaccio de ternera", "second_course": "Pizza Quattro Formaggi", "dessert": "Panna Cotta", "price": 14.50},
            {"date": "2026-02-19", "first_course": "Antipasti de burrata con tomates cherry", "second_course": "Pizza Prosciutto e Funghi", "dessert": "Cannoli siciliano", "price": 16.00},
            {"date": "2026-02-20", "first_course": "Antipasti de vitello tonnato", "second_course": "Pizza Diavola", "dessert": "Gelato artesanal", "price": 15.50},
            {"date": "2026-02-21", "first_course": "Antipasti de ensalada Caprese", "second_course": "Pizza Napolitana", "dessert": "Tarta de limón", "price": 15.00},
            {"date": "2026-02-22", "first_course": "Antipasti misto de verduras asadas", "second_course": "Pizza Calzone", "dessert": "Profiteroles", "price": 16.50},
            {"date": "2026-02-23", "first_course": "Antipasti de focaccia con tomate y orégano", "second_course": "Pizza Pepperoni", "dessert": "Mousse de chocolate", "price": 14.00},
            {"date": "2026-02-24", "first_course": "Antipasti de carpaccio de salmón", "second_course": "Pizza Quattro Stagioni", "dessert": "Semifrío de vainilla", "price": 16.00},
            {"date": "2026-02-25", "first_course": "Antipasti de alcachofas a la romana", "second_course": "Pizza Hawaiana", "dessert": "Tiramisú de fresa", "price": 15.50},
            {"date": "2026-02-26", "first_course": "Antipasti de gazpacho italiano", "second_course": "Pizza Funghi", "dessert": "Panna Cotta de frutos rojos", "price": 14.50},
            {"date": "2026-02-27", "first_course": "Antipasti de bruschetta de salmón", "second_course": "Pizza Marinara", "dessert": "Cannoli de pistacho", "price": 17.00},
            {"date": "2026-02-28", "first_course": "Antipasti de prosciutto con melón", "second_course": "Pizza Vegetal", "dessert": "Gelato de stracciatella", "price": 16.50},
            {"date": "2026-03-01", "first_course": "Antipasti de crema de calabaza", "second_course": "Pizza BBQ", "dessert": "Tarta de manzana", "price": 14.00},
            {"date": "2026-03-02", "first_course": "Antipasti de ensalada de rúcula y parmesano", "second_course": "Pizza Trufa y Parmesano", "dessert": "Mousse de limoncello", "price": 15.50},
            {"date": "2026-03-03", "first_course": "Antipasti de berenjena a la parmigiana", "second_course": "Pizza Caprichosa", "dessert": "Profiteroles de chocolate", "price": 15.00},
            {"date": "2026-03-04", "first_course": "Antipasti de sopa Minestrone", "second_course": "Pizza Siciliana", "dessert": "Semifrío de café", "price": 16.00},
            {"date": "2026-03-05", "first_course": "Antipasti de crema de espárragos", "second_course": "Pizza Tonno e Cipolla", "dessert": "Tiramisú clásico", "price": 15.50},
            {"date": "2026-03-06", "first_course": "Antipasti de bruschetta de tomate y albahaca", "second_course": "Pizza Romana", "dessert": "Gelato de limón", "price": 14.50},
            {"date": "2026-03-07", "first_course": "Antipasti de pulpo a la gallega", "second_course": "Pizza Bianca con rúcula", "dessert": "Cannoli de chocolate", "price": 16.50},
            {"date": "2026-03-08", "first_course": "Antipasti de crema de champiñones", "second_course": "Pizza Prosciutto Crudo", "dessert": "Panna Cotta de mango", "price": 15.00},
            {"date": "2026-03-09", "first_course": "Antipasti de focaccia rellena de jamón", "second_course": "Pizza Mediterránea", "dessert": "Mousse de maracuyá", "price": 15.50},
            {"date": "2026-03-10", "first_course": "Antipasti de carpaccio de calabacín", "second_course": "Pizza Bufala", "dessert": "Tarta Caprese de chocolate", "price": 17.00},
            {"date": "2026-03-11", "first_course": "Antipasti de sopa Toscana", "second_course": "Pizza Salsiccia e Friarielli", "dessert": "Gelato de pistacho", "price": 15.00},
            {"date": "2026-03-12", "first_course": "Antipasti de ensalada tibia de verduras", "second_course": "Pizza Margherita Especial", "dessert": "Tiramisú de pistacho", "price": 14.50},
            {"date": "2026-03-13", "first_course": "Antipasti de bruschetta de berenjena", "second_course": "Pizza al Taglio", "dessert": "Panna Cotta de caramelo", "price": 15.00},
            {"date": "2026-03-14", "first_course": "Antipasti de tartar de atún", "second_course": "Pizza Tartufata", "dessert": "Semifrío de avellana", "price": 18.00},
            {"date": "2026-03-15", "first_course": "Antipasti de gazpacho de remolacha", "second_course": "Pizza Ortolana", "dessert": "Profiteroles de nata", "price": 15.50},
            {"date": "2026-03-16", "first_course": "Antipasti de vitello tonnato", "second_course": "Pizza Amatriciana", "dessert": "Mousse de chocolate blanco", "price": 16.00},
            {"date": "2026-03-17", "first_course": "Antipasti de burrata con pesto", "second_course": "Pizza de Mariscos", "dessert": "Cannoli de ricotta", "price": 17.50},
        ]
        for m in menus:
            db.add(Menu(**m))
        db.commit()
        print(f"{len(menus)} menús semilla insertados")
    db.close()

seed_menus()
