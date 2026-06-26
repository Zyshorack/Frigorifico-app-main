# 5.2 Registrar salida de stock FIFO

## Objetivo

Implementar el flujo para registrar una salida de mercaderia usando FIFO.
FIFO significa First In, First Out: primero sale lo que entro primero. Ademas, los lotes vencidos no se usan para salidas normales.

## Endpoint

POST /stock/exit

## Archivos involucrados

- app/controller/stock.py
- app/dto/stock.py
- app/services/stock_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con salidas de stock.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service valida que el producto exista.
4. Si se informa cold_location_id, valida que la camara exista.
5. Busca lotes con status active, no vencidos y con cantidad restante.
6. Ordena los lotes por fecha de ingreso para cumplir FIFO.
7. Si el stock disponible no alcanza, responde HTTP 409 Conflict.
8. Consume primero el lote mas antiguo.
9. Si un lote queda sin cantidad, cambia su estado a exhausted.
10. Crea uno o mas StockMovement de tipo exit.
11. Devuelve cantidad solicitada, cantidad consumida y movimientos generados.

## Response

Implementar response_model con StockExitResult de ser necesario.

## Campos principales:

requested_quantity
consumed_quantity
movements

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar POST /stock/exit desde Swagger despues de crear lotes.

## Resultado esperado:

La salida consume lotes no vencidos.
Se consume primero el lote mas antiguo.
Si no hay stock suficiente, responde HTTP 409.

### Request

```json
{
  "product_id": 1,
  "cold_location_id": 1,
  "quantity": 5,
  "user_id": 1,
  "description": "Salida de prueba"
}
```
