# 2 - Arquitectura

El proyecto usa una arquitectura por capas con FastAPI, SQLAlchemy, Pydantic y SQLite.

La separacion busca que cada parte tenga una responsabilidad clara: los controllers reciben requests, los services aplican reglas de negocio, los repositories acceden a base de datos y los models representan las tablas.

## Estructura principal

```text
app/
|- core/
|- controller/
|- services/
|- repositories/
|- models/
|- dto/
|- enums/
|- db/
`- static/
```

## Responsabilidades

- `core`: centraliza configuracion y utilidades transversales como seguridad basica.
- `controller`: define endpoints HTTP y delega la logica.
- `services`: contiene casos de uso y reglas del sistema.
- `repositories`: encapsula consultas reutilizables y operaciones de persistencia simples.
- `models`: define entidades SQLAlchemy.
- `dto`: define contratos de entrada y salida de la API.
- `enums`: centraliza codigos conocidos del dominio.
- `db`: configura la conexion, session y base declarativa.
- `static`: contiene una interfaz HTML, CSS y JavaScript simple para probar la API.
- `tests`: contiene pruebas automaticas de flujos criticos.

## Organizacion por dominio

Aunque el codigo actual usa archivos simples, el dominio se puede leer en estas areas:

- `users`: usuarios, roles y login simple.
- `products`: categorias, productos y catalogo disponible.
- `cold`: camaras, sensores y lecturas.
- `alerts`: alertas y acciones correctivas.
- `stock`: lotes, movimientos y regla FIFO.

## Flujo de request

```text
HTTP request
  -> controller
  -> DTO de entrada
  -> service
  -> repository/model
  -> base de datos
  -> DTO de salida
  -> HTTP response
```

## Base de datos

La base se crea con `Base.metadata.create_all` cuando inicia la aplicacion.

Esto es practico para principiantes porque evita configurar migraciones al inicio. Para un proyecto mas avanzado, el siguiente paso natural seria agregar Alembic, como en `rental-api`.

## Decisiones didacticas

- Se usa SQLite por simplicidad.
- Se conserva una estructura por capas para que sea facil migrar a MySQL o PostgreSQL.
- Las reglas importantes viven en services, no en controllers.
- Los issues estan escritos por endpoint para que cada tarea tenga un alcance claro.
