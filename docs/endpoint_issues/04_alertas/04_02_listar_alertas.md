# 4.2 Listar alertas

## Objetivo

Implementar el flujo para consultar alertas operativas.
Este endpoint permite ver alertas abiertas, reconocidas o resueltas, y tambien filtrar por estado.

## Endpoint

GET /alerts

## Archivos involucrados

- app/controller/alerts.py
- app/dto/alerts.py
- app/services/alert_service.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el listado de alertas.

El flujo esperado es:

1. El controller recibe la request.
2. El controller puede recibir el query param status.
3. El controller llama al service.
4. El service arma la consulta ordenando por fecha descendente.
5. Si viene status, filtra por ese estado.
6. Devuelve la lista de alertas.

## Response

Implementar response_model con list[AlertRead] de ser necesario.

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

Probar GET /alerts?status=open desde Swagger.

## Resultado esperado:

Devuelve una lista de alertas.
Si se informa status, devuelve solo alertas de ese estado.
Las alertas aparecen ordenadas desde la mas reciente.
