# Endpoints minimos para probar el flujo operativo

Este documento muestra un recorrido minimo para probar el sistema desde Swagger.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 1. Crear usuario

Endpoint:

```text
POST /users
```

Body sugerido:

```json
{
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}
```

## 2. Iniciar sesion

Endpoint:

```text
POST /users/login
```

Body sugerido:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

## 3. Crear producto

Endpoint:

```text
POST /products
```

Body sugerido:

```json
{
  "name": "Media res",
  "description": "Producto bovino para camara",
  "unit": "kg"
}
```

Guardar el `id` devuelto.

## 4. Crear camara de frio

Endpoint:

```text
POST /cold-locations
```

Body sugerido:

```json
{
  "name": "Camara 1",
  "min_temperature": 0,
  "max_temperature": 5,
  "min_humidity": 40,
  "max_humidity": 75
}
```

Guardar el `id` devuelto.

## 5. Crear sensor

Endpoint:

```text
POST /sensors
```

Body sugerido:

```json
{
  "cold_location_id": 1,
  "name": "Sensor Camara 1",
  "sensor_type": "mixed"
}
```

## 6. Registrar lectura fuera de rango

Endpoint:

```text
POST /sensors/{sensor_id}/readings
```

Body sugerido:

```json
{
  "temperature": 8.5,
  "humidity": 60
}
```

Resultado esperado:

- se guarda la lectura;
- se crea una alerta abierta de temperatura.

## 7. Consultar alertas abiertas

Endpoint:

```text
GET /alerts?status=open
```

Guardar el `id` de la alerta.

## 8. Resolver alerta

Endpoint:

```text
PATCH /alerts/{alert_id}/status
```

Body sugerido:

```json
{
  "status": "resolved"
}
```

## 9. Registrar entrada de stock

Endpoint:

```text
POST /stock/entry
```

Body sugerido:

```json
{
  "product_id": 1,
  "cold_location_id": 1,
  "quantity": 20,
  "expiration_date": "2026-12-31",
  "description": "Ingreso inicial"
}
```

## 10. Registrar salida FIFO

Endpoint:

```text
POST /stock/exit
```

Body sugerido:

```json
{
  "product_id": 1,
  "cold_location_id": 1,
  "quantity": 5,
  "description": "Salida de prueba"
}
```

Resultado esperado:

- se consume stock de lotes activos no vencidos;
- se generan movimientos de salida;
- se actualiza la cantidad restante del lote.

## 11. Consultar catalogo disponible

Endpoint:

```text
GET /catalog
```

Resultado esperado:

- devuelve productos activos;
- muestra `available_quantity` calculado desde lotes activos no vencidos.
