# 2.3 Crear producto

## Objetivo

Implementar el flujo para registrar un producto del frigorifico.
El producto representa mercaderia que luego puede tener lotes de stock, por ejemplo:
- Media res
- Nalga
- Pollo entero
- Caja de hamburguesas

## Endpoint

POST /products

## Archivos involucrados

- app/controller/products.py
- app/dto/products.py
- app/services/product_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la creacion de productos.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service valida si ya existe un producto con el mismo nombre.
4. Si ya existe, responde HTTP 409 Conflict.
5. Si se informa category_id, valida que la categoria exista.
6. Si la categoria no existe, responde HTTP 404 Not Found.
7. Crea el producto y lo devuelve.

## Response

Implementar response_model con ProductRead de ser necesario.

## Campos principales:

id
category_id
name
description
unit

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar POST /products desde Swagger.

## Resultado esperado:

Se crea un producto valido.
Si el nombre ya existe, responde HTTP 409.
Si la categoria informada no existe, responde HTTP 404.

### Request

```json
{
  "name": "Media res",
  "category_id": 1,
  "description": "Producto bovino refrigerado",
  "unit": "kg"
}
```
