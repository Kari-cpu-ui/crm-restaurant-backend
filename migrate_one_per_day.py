"""
Reorganizar menús: 1 pizza por día, alternando los 9 tipos de pizza,
desde 2026-02-17 hasta dentro de un mes (2026-03-19).
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import date, timedelta

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

# Las 9 pizzas base (nombre, descripcion, precio, category_id, image_url)
pizzas = [
    ("Margarita", "Tomate, mozzarella y albahaca", 8.5, 1, "assets/images/pizza-margarita.png"),
    ("Pepperoni", "Pepperoni y mozzarella", 9.5, 1, "assets/images/pizza-pepperoni.png"),
    ("Cuatro Quesos", "Mozzarella, gorgonzola, parmesano, cheddar", 10.0, 1, "assets/images/pizza-cuatro-quesos.png"),
    ("Burrata & Trufa", "Burrata fresca con aceite de trufa", 13.5, 2, "assets/images/pizza-burrata.png"),
    ("Prosciutto", "Jamón italiano y rúcula", 12.5, 2, "assets/images/pizza-prosciutto.png"),
    ("Pesto & Pollo", "Pollo grillado y pesto casero", 11.5, 2, "assets/images/pizza-pesto-pollo.png"),
    ("Vegetariana", "Verduras asadas", 9.0, 3, "assets/images/pizza-vegetariana.png"),
    ("BBQ Vegana", "Proteína vegetal y salsa BBQ", 10.0, 3, "assets/images/pizza-bbq-vegana.png"),
    ("Espinaca & Ricotta", "Espinaca fresca y ricotta", 9.5, 3, "assets/images/pizza-espinaca-ricotta.png"),
]

# Generar fechas: desde 17 feb hasta 19 mar (31 días)
start_date = date(2026, 2, 17)
num_days = 31

with engine.connect() as conn:
    # 1. Borrar todos los menús existentes
    conn.execute(text("DELETE FROM pizzas"))
    conn.commit()
    print("Menús anteriores eliminados.")

    # 2. Insertar 1 pizza por día, alternando las 9 pizzas
    for i in range(num_days):
        pizza = pizzas[i % len(pizzas)]
        menu_date = start_date + timedelta(days=i)
        conn.execute(
            text(
                "INSERT INTO pizzas (name, description, price, category_id, is_active, image_url, menu_date) "
                "VALUES (:name, :desc, :price, :cat, 1, :img, :mdate)"
            ),
            {
                "name": pizza[0],
                "desc": pizza[1],
                "price": pizza[2],
                "cat": pizza[3],
                "img": pizza[4],
                "mdate": menu_date.strftime("%Y-%m-%d"),
            }
        )
    conn.commit()
    print(f"{num_days} menús creados (1 por día, del {start_date} al {start_date + timedelta(days=num_days-1)}).")

    # 3. Verificar resultado
    r = conn.execute(text("SELECT id, name, menu_date FROM pizzas ORDER BY menu_date"))
    for row in r:
        print(f"  {row[2]} - {row[1]}")

print("Migración completada.")
