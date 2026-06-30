# Frigorifico API

API base para un sistema de control frigorifico orientado a principiantes.
Incluye una aplicacion web integrada servida por FastAPI desde `app/static`.

El proyecto utiliza FastAPI, SQLAlchemy, SQLite por defecto, Pydantic y Pytest. El objetivo es practicar una API por capas con un dominio operativo real: usuarios, productos, camaras de frio, sensores, alertas, lotes y stock FIFO.

## Requisitos

- Python 3.11 o superior
- PowerShell

SQLite se usa por defecto para evitar instalaciones adicionales. La base se crea automaticamente al levantar la aplicacion.

## Como levantar el proyecto

Ejecutar los comandos desde la carpeta raiz del proyecto.

1. Crear el entorno virtual:

```powershell
python -m venv .venv
```

2. Instalar dependencias:

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

3. Levantar la API:

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Al iniciar, la aplicacion crea las tablas necesarias con SQLAlchemy si todavia no existen y agrega columnas nuevas compatibles con SQLite cuando faltan.

## URLs utiles

- Aplicacion web integrada: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

Si el puerto 8000 ya esta ocupado, levantar Uvicorn con otro puerto, por ejemplo:

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

## Documentacion

- `docs/README.md`: indice de documentacion escrita.
- `docs/01_objetivo.md`: objetivo funcional del sistema.
- `docs/02_arquitectura.md`: arquitectura por capas.
- `docs/03_entidades_del_sistema.md`: entidades principales del dominio.
- `docs/endpoints_minimos_flujo_operativo.md`: flujo minimo para probar desde Swagger.
- `docs/endpoint_issues/`: issues por endpoint, organizados por nivel.

## Gestion del aprendizaje

El proyecto esta organizado para que cada issue represente una tarea chica y concreta.

La regla didactica recomendada es:

```text
1 issue = 1 endpoint = controller + DTO + service + repository si hace falta + prueba manual
```

## Base de datos

Por defecto se usa SQLite.

La ubicacion se define desde `app/core/config.py`:

- si existe `DATABASE_URL`, se usa ese valor;
- si existe `CONTROL_FRIGORIFICO_DATA_DIR`, se usa esa carpeta;
- en Windows, si no hay configuracion, se crea `%LOCALAPPDATA%\ControlFrigorifico\frigorifico.db`;
- en otros sistemas, se usa `data/frigorifico.db` dentro del proyecto;


## Datos seed

Al iniciar la aplicacion se cargan datos iniciales idempotentes si no existen:

- categorias `Carnes bovinas` y `Embutidos`;
- productos `Media res`, `Asado`, `Nalga` y `Chorizo fresco`;
- una camara seed para stock inicial;
- lotes activos con vencimientos futuros y movimientos de entrada asociados.

El seed no duplica productos ni lotes si ya fueron creados previamente.
## Endpoints principales

- `POST /users`
- `POST /users/login`
- `GET /users`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`
- `POST /categories`
- `GET /categories`
- `PATCH /categories/{category_id}`
- `DELETE /categories/{category_id}`
- `POST /products`
- `GET /products`
- `PATCH /products/{product_id}`
- `DELETE /products/{product_id}`
- `GET /catalog`
- `POST /cold-locations`
- `GET /cold-locations`
- `PATCH /cold-locations/{location_id}`
- `DELETE /cold-locations/{location_id}`
- `POST /sensors`
- `GET /sensors`
- `PATCH /sensors/{sensor_id}`
- `DELETE /sensors/{sensor_id}`
- `POST /sensors/{sensor_id}/readings`
- `POST /alerts`
- `GET /alerts`
- `PATCH /alerts/{alert_id}`
- `PATCH /alerts/{alert_id}/status`
- `DELETE /alerts/{alert_id}`
- `POST /stock/entry`
- `POST /stock/exit`
- `GET /stock/batches`
- `PATCH /stock/batches/{batch_id}`
- `DELETE /stock/batches/{batch_id}`

## Pruebas

```powershell
.\.venv\Scripts\python -m pytest
```

Las pruebas actuales cubren dos reglas importantes:

- login y gestion basica de usuarios;
- una lectura fuera de rango crea alerta;
- una salida de stock consume lotes no vencidos usando FIFO.
- productos, usuarios y lotes aplican modificacion y borrado logico.

## Problemas comunes

Si aparece un error de dependencias, reinstalar desde `requirements.txt`.

Si se quiere reiniciar la base SQLite local en Windows, cerrar la API y eliminar `%LOCALAPPDATA%\ControlFrigorifico\frigorifico.db`. No borrar datos reales si el proyecto ya se esta usando con informacion importante.


