# 2.4 Listar productos

## Objetivo

Implementar el flujo para consultar los productos registrados.
Este endpoint permite revisar el catalogo base sin calcular stock disponible.

## Endpoint

GET /products

## Archivos involucrados

- app/controller/products.py
- app/dto/products.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el listado de productos.

El flujo esperado es:

1. El controller recibe la request.
2. El controller obtiene la sesion de base de datos.
3. Se consultan los productos registrados.
4. Se devuelve una lista usando ProductRead.
5. La response muestra datos basicos del producto.

## Response

Implementar response_model con list[ProductRead] de ser necesario.

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

Probar GET /products desde Swagger.

## Resultado esperado:

Devuelve una lista de productos.
Cada producto muestra unidad y categoria si tiene.
Si no hay productos, devuelve una lista vacia.
