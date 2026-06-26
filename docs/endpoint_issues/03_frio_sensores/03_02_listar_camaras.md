# 3.2 Listar camaras

## Objetivo

Implementar el flujo para consultar camaras o zonas de frio registradas.
Este endpoint permite revisar las camaras disponibles antes de asociar sensores o lotes.

## Endpoint

GET /cold-locations

## Archivos involucrados

- app/controller/cold.py
- app/dto/cold.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el listado de camaras.

El flujo esperado es:

1. El controller recibe la request.
2. El controller obtiene la sesion de base de datos.
3. Se consultan las camaras registradas.
4. Se devuelve una lista usando ColdLocationRead.
5. La response muestra rangos configurados.

## Response

Implementar response_model con list[ColdLocationRead] de ser necesario.

## Campos principales:

id
name
description
min_temperature
max_temperature
min_humidity
max_humidity

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar GET /cold-locations desde Swagger.

## Resultado esperado:

Devuelve una lista de camaras.
Cada camara muestra sus rangos.
Si no hay camaras, devuelve una lista vacia.
