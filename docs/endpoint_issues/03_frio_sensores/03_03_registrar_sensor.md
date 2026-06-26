# 3.3 Registrar sensor

## Objetivo

Implementar el flujo para registrar un sensor asociado a una camara o zona de frio.
El sensor permite cargar lecturas de temperatura y humedad para controlar si la camara trabaja dentro de rango.

## Endpoint

POST /sensors

## Archivos involucrados

- app/controller/cold.py
- app/dto/sensors.py
- app/services/cold_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la creacion de sensores.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service valida que exista la camara indicada por cold_location_id.
4. Si la camara no existe, responde HTTP 404 Not Found.
5. Si existe, crea el sensor activo.
6. El sensor queda asociado a la camara indicada.

## Response

Implementar response_model con SensorRead de ser necesario.

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

Probar POST /sensors desde Swagger.

## Resultado esperado:

Se crea un sensor valido asociado a una camara.
Si la camara no existe, responde HTTP 404.
El sensor queda disponible para registrar lecturas.

### Request

```json
{
  "cold_location_id": 1,
  "name": "Sensor Camara 1",
  "sensor_type": "mixed"
}
```
