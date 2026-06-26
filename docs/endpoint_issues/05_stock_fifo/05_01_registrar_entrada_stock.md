# 5.1 Registrar entrada de stock

## Objetivo

Implementar el flujo para registrar una entrada de mercaderia.
Cada entrada crea un lote nuevo con cantidad, vencimiento y ubicacion opcional.

## Endpoint

POST /stock/entry

## Archivos involucrados

- app/controller/stock.py
- app/dto/stock.py
- app/services/stock_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con entradas de stock.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service valida que el producto exista.
4. Si se informa cold_location_id, valida que la camara exista.
5. Crea un Batch con quantity y remaining_quantity iguales.
6. Crea un StockMovement de tipo entry.
7. Devuelve el lote creado.

## Response

Implementar response_model con BatchRead de ser necesario.

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

Probar POST /stock/entry desde Swagger.

## Resultado esperado:

Se crea un lote valido.
La cantidad restante queda igual a la cantidad ingresada.
Se registra un movimiento de entrada.

### Request

```json
{
  "product_id": 1,
  "cold_location_id": 1,
  "quantity": 20,
  "expiration_date": "2026-12-31",
  "user_id": 1,
  "description": "Ingreso inicial"
}
```
