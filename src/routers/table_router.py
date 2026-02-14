from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from src.models.table_model import Table
from src.schemas.table_schema import TableCreate, TableRead, TableUpdate

# Router independiente para mesas
router = APIRouter(
    prefix="/tables",   # Todas las rutas empiezan con /tables
    tags=["Tables"]     # Se ve en docs como "Tables"
)

# Dependencia para la sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Listar todas las mesas
@router.get("/", response_model=list[TableRead])
def get_tables(db: Session = Depends(get_db)):
    """
    Devuelve todas las mesas registradas en la base de datos
    """
    return db.query(Table).all()

# Crear una mesa nueva

@router.post("/", response_model=TableRead)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva mesa con nombre y capacidad
    """
    db_table = Table(**table.dict())  # Crear objeto ORM a partir del schema
    db.add(db_table)                  # Preparar INSERT
    db.commit()                       # Ejecutar INSERT
    db.refresh(db_table)              # Recargar objeto para obtener ID
    return db_table                   # Retornar la mesa creada

# Actualizar una mesa existente

@router.put("/{table_id}", response_model=TableRead)
def update_table(table_id: int, table_update: TableUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de una mesa existente (nombre o capacidad)
    """
    table = db.query(Table).filter(Table.id == table_id).first()  # Buscar la mesa
    if not table:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")

    # Actualizar solo los campos que vienen en el request
    if table_update.name is not None:
        table.name = table_update.name
    if table_update.capacity is not None:
        table.capacity = table_update.capacity

    db.commit()        # Guardar cambios en la DB
    db.refresh(table)  # Refrescar objeto
    return table       # Retornar la mesa actualizada
