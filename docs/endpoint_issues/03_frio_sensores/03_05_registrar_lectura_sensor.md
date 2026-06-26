# 3.5 Registrar lectura de sensor

## Objetivo

Implementar el flujo para registrar una lectura de temperatura y humedad.
La lectura queda como historial operativo. Si esta fuera de rango, el backend crea una alerta automaticamente.

## Endpoint

POST /sensors/{sensor_id}/readings

## Archivos involucrados

- app/controller/cold.py
- app/dto/sensors.py
- app/services/cold_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la creacion de lecturas de sensor.

El flujo esperado es:

1. El controller recibe sensor_id por path y la lectura por body.
2. El controller llama al service.
3. El service busca el sensor activo.
4. Si el sensor no existe o no esta activo, responde HTTP 404 Not Found.
5. Guarda la lectura con temperatura, humedad y fecha.
6. Compara la lectura contra los rangos del sensor o de la camara.
7. Si temperatura o humedad quedan fuera de rango, crea una alerta abierta.

## Response

Implementar response_model con SensorReadingRead de ser necesario.

## Campos principales:

id
device_id
temperature
humidity
recorded_at

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar POST /sensors/{sensor_id}/readings desde Swagger.

## Resultado esperado:

Se crea una lectura valida.
Si la lectura esta dentro de rango, no se crea alerta.
Si la lectura esta fuera de rango, se crea una alerta abierta.

### Request

```json
{
  "temperature": 8.5,
  "humidity": 60
}
```
