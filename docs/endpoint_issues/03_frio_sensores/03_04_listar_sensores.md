# 3.4 Listar sensores

## Objetivo

Implementar el flujo para consultar sensores registrados.
Este endpoint permite revisar que sensores existen y a que camara pertenece cada uno.

## Endpoint

GET /sensors

## Archivos involucrados

- app/controller/cold.py
- app/dto/sensors.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el listado de sensores.

El flujo esperado es:

1. El controller recibe la request.
2. El controller obtiene la sesion de base de datos.
3. Se consultan los sensores registrados.
4. Se devuelve una lista usando SensorRead.
5. La response mantiene visible la relacion con cold_location_id.

## Response

Implementar response_model con list[SensorRead] de ser necesario.

## Campos principales:

id
cold_location_id
name
sensor_type
is_active

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar GET /sensors desde Swagger.

## Resultado esperado:

Devuelve una lista de sensores.
Cada sensor indica a que camara pertenece.
Si no hay sensores, devuelve una lista vacia.
