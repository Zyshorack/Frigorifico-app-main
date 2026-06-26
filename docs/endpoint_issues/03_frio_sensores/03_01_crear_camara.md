# 3.1 Crear camara o zona de frio

## Objetivo

Implementar el flujo para registrar una camara, freezer, heladera o zona de frio.
La camara define rangos esperados de temperatura y humedad para controlar la mercaderia.

## Endpoint

POST /cold-locations

## Archivos involucrados

- app/controller/cold.py
- app/dto/cold.py
- app/services/cold_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la creacion de camaras de frio.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service crea una ColdLocation con los datos recibidos.
4. Se guardan los rangos de temperatura y humedad si fueron informados.
5. Devuelve la camara creada.

## Response

Implementar response_model con ColdLocationRead de ser necesario.

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

Probar POST /cold-locations desde Swagger.

## Resultado esperado:

Se crea una camara valida.
Los rangos quedan registrados.
La camara queda disponible para asociar sensores y lotes.

### Request

```json
{
  "name": "Camara 1",
  "description": "Camara principal",
  "min_temperature": 0,
  "max_temperature": 5,
  "min_humidity": 40,
  "max_humidity": 75
}
```
