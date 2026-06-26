# 4.1 Crear alerta manual

## Objetivo

Implementar el flujo para registrar una alerta manual.
La alerta manual sirve cuando un operador detecta un problema que no vino automaticamente desde un sensor.

## Endpoint

POST /alerts

## Archivos involucrados

- app/controller/alerts.py
- app/dto/alerts.py
- app/services/alert_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la creacion manual de alertas.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service crea una alerta con tipo, severidad y mensaje.
4. La alerta queda con estado inicial open.
5. Devuelve la alerta creada.

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

Probar POST /alerts desde Swagger.

## Resultado esperado:

Se crea una alerta manual valida.
La alerta queda abierta.
La alerta puede consultarse luego desde GET /alerts.

### Request

```json
{
  "alert_type": "manual",
  "severity": "medium",
  "message": "Puerta de camara abierta por revision",
  "cold_location_id": 1
}
```
