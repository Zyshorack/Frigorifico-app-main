# 5.3 Listar lotes

## Objetivo

Implementar el flujo para consultar lotes registrados.
Este endpoint sirve para verificar entradas, salidas FIFO, cantidades restantes y estados de los lotes.

## Endpoint

GET /stock/batches

## Archivos involucrados

- app/controller/stock.py
- app/dto/stock.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el listado de lotes.

El flujo esperado es:

1. El controller recibe la request.
2. El controller obtiene la sesion de base de datos.
3. Se consultan los lotes registrados.
4. Se devuelve una lista usando BatchRead.
5. La response permite revisar quantity, remaining_quantity y status.

## Response

Implementar response_model con list[BatchRead] de ser necesario.

## Campos principales:

id
product_id
cold_location_id
quantity
remaining_quantity
entry_date
expiration_date
status

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar GET /stock/batches desde Swagger.

## Resultado esperado:

Devuelve una lista de lotes.
Cada lote muestra cantidad inicial y cantidad restante.
Despues de una salida FIFO, se ve actualizado remaining_quantity.
