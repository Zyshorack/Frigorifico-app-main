# 2.1 Crear categoria de producto

## Objetivo

Implementar el flujo para registrar una categoria de producto.
La categoria sirve para agrupar productos dentro del catalogo, por ejemplo:
- Carnes
- Lacteos
- Congelados
- Bebidas

## Endpoint

POST /categories

## Archivos involucrados

- app/controller/products.py
- app/dto/products.py
- app/services/product_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la creacion de categorias.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service valida si ya existe una categoria con el mismo nombre.
4. Si ya existe, responde HTTP 409 Conflict.
5. Si no existe, crea la categoria.
6. Devuelve la categoria creada.

## Response

Implementar response_model de ser necesario.

## Campos principales:

id
name
description

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar POST /categories desde Swagger.

## Resultado esperado:

Se crea una categoria valida.
Si ya existe una categoria con el mismo nombre, responde HTTP 409.
La categoria queda registrada correctamente.

### Request

```json
{
  "name": "Carnes",
  "description": "Productos carnicos refrigerados"
}
```
