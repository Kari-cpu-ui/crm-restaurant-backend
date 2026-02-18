"""
Actualizar los image_url de los menús para que coincidan
con las imágenes reales del frontend.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

# Mapeo: nombre de pizza -> imagen real en el frontend
image_map = {
    "Margarita": "assets/images/pizza-margarita.png",
    "Pepperoni": "assets/images/peperoni.png",
    "Cuatro Quesos": "assets/images/4-quesos.png",
    "Burrata & Trufa": "assets/images/burrata-con-cherry.png",
    "Prosciutto": "assets/images/proscuitto.png",
    "Pesto & Pollo": "assets/images/pesto-y-pollo.png",
    "Vegetariana": "assets/images/vegetal.png",
    "BBQ Vegana": "assets/images/vegetal.png",
    "Espinaca & Ricotta": "assets/images/espinaca-y-ricota.png",
}

with engine.connect() as conn:
    for name, img in image_map.items():
        conn.execute(
            text("UPDATE pizzas SET image_url = :img WHERE name = :name"),
            {"img": img, "name": name}
        )
        print(f"  {name} -> {img}")
    conn.commit()

    # Verificar
    r = conn.execute(text("SELECT name, image_url FROM pizzas ORDER BY menu_date"))
    print("\nResultado:")
    for row in r:
        print(f"  {row[0]}: {row[1]}")

print("\nImágenes actualizadas.")
