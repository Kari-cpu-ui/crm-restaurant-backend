"""Migración: Añadir reservation_code a reservations y reemplazar reservation_id por reservation_code en reviews"""
import random
from db import engine
from sqlalchemy import text

with engine.connect() as conn:
    # 1. Añadir columna reservation_code a reservations (sin UNIQUE aún)
    conn.execute(text("ALTER TABLE reservations ADD COLUMN reservation_code VARCHAR(4) NULL"))
    print("Columna reservation_code añadida a reservations")

    # 2. Generar códigos únicos para reservas existentes
    rows = conn.execute(text("SELECT id FROM reservations")).fetchall()
    used_codes = set()
    for row in rows:
        while True:
            code = f"{random.randint(0, 9999):04d}"
            if code not in used_codes:
                used_codes.add(code)
                break
        conn.execute(text("UPDATE reservations SET reservation_code = :code WHERE id = :id"), {"code": code, "id": row[0]})
    print(f"Códigos generados para {len(rows)} reservas existentes")

    # 3. Hacer la columna NOT NULL y UNIQUE
    conn.execute(text("ALTER TABLE reservations MODIFY COLUMN reservation_code VARCHAR(4) NOT NULL"))
    conn.execute(text("ALTER TABLE reservations ADD UNIQUE INDEX uq_reservation_code (reservation_code)"))
    print("Columna reservation_code ahora es NOT NULL UNIQUE")

    # 4. Eliminar FK de reviews.reservation_id
    fk_rows = conn.execute(text(
        "SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE "
        "WHERE TABLE_NAME = 'reviews' AND COLUMN_NAME = 'reservation_id' "
        "AND REFERENCED_TABLE_NAME IS NOT NULL"
    )).fetchall()
    for fk in fk_rows:
        conn.execute(text(f"ALTER TABLE reviews DROP FOREIGN KEY {fk[0]}"))
        print(f"FK {fk[0]} eliminada de reviews")

    # 5. Añadir columna reservation_code a reviews y migrar datos
    conn.execute(text("ALTER TABLE reviews ADD COLUMN reservation_code VARCHAR(4) NULL"))
    conn.execute(text(
        "UPDATE reviews r JOIN reservations res ON r.reservation_id = res.id "
        "SET r.reservation_code = res.reservation_code"
    ))
    print("Datos migrados de reservation_id a reservation_code en reviews")

    # 6. Eliminar columna reservation_id y hacer reservation_code NOT NULL con FK
    conn.execute(text("ALTER TABLE reviews DROP COLUMN reservation_id"))
    conn.execute(text("ALTER TABLE reviews MODIFY COLUMN reservation_code VARCHAR(4) NOT NULL"))
    conn.execute(text(
        "ALTER TABLE reviews ADD CONSTRAINT fk_reviews_reservation_code "
        "FOREIGN KEY (reservation_code) REFERENCES reservations(reservation_code)"
    ))
    print("FK reservation_code creada en reviews")

    conn.commit()
    print("Migración completada exitosamente!")
