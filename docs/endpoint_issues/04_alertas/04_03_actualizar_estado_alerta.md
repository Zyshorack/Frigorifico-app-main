# 4.3 Actualizar estado de alerta

## Objetivo

Implementar el flujo para actualizar el estado de una alerta.
Por ahora el modelo es simple: la alerta solo guarda status y resolved_at.

## Endpoint

PATCH /alerts/{alert_id}/status

## Archivos involucrados

- app/controller/alerts.py
- app/dto/alerts.py
- app/services/alert_service.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la actualizacion de estado de alertas.

El flujo esperado es:

1. El controller recibe alert_id por path y el nuevo estado por body.
2. El controller llama al service.
3. El service busca la alerta.
4. Si no existe, responde HTTP 404 Not Found.
5. Actualiza alert.status con el nuevo estado.
6. Si el estado es resolved, carga resolved_at.

## Response

Implementar response_model con AlertRead de ser necesario.

## Campos principales:

id
device_id
cold_location_id
alert_type
severity
status
message
created_at
resolved_at

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar PATCH /alerts/{alert_id}/status desde Swagger.

## Resultado esperado:

Una alerta puede cambiar de estado.
Si pasa a resolved, queda registrada la fecha resolved_at.

### Request

```json
{
  "status": "resolved"
}
```
