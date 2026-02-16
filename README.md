# CRM Restaurante - Backend

API REST para la gestión de un restaurante, desarrollada con **FastAPI**.

## Requisitos

- Python 3.11+
- MySQL

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd crm-restaurant-backend
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python -m venv .venv
   ```

   - Windows:
     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```



El servidor se iniciará en `http://127.0.0.1:8000`.

## Documentación de la API

Una vez el servidor esté corriendo, puedes acceder a la documentación interactiva:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Estructura del proyecto

```
├── main.py                  # Punto de entrada de la aplicación
├── auth.py                  # Autenticación y JWT
├── db.py                    # Conexión a la base de datos
├── requirements.txt         # Dependencias
├── src/
│   ├── controllers/         # Lógica de negocio
│   ├── models/              # Modelos SQLAlchemy (ORM)
│   ├── routers/             # Rutas de la API
│   └── schemas/             # Esquemas Pydantic (validación)
```
