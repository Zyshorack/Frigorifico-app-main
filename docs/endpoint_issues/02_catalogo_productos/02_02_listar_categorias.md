# 2.2 Listar categorias

## Objetivo

Implementar el flujo para consultar las categorias de productos.
Este endpoint ayuda a revisar que grupos de productos existen antes de crear nuevos productos.

## Endpoint

GET /categories

## Archivos involucrados

- app/controller/products.py
- app/dto/products.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el listado de categorias.

El flujo esperado es:

1. El controller recibe la request.
2. El controller obtiene la sesion de base de datos.
3. Se consultan las categorias registradas.
4. Se devuelve una lista usando el DTO de response.
5. Swagger muestra el contrato de salida.

## Response

Implementar response_model con list[ProductCategoryRead] de ser necesario.

## Campos principales:

id
name
description

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar GET /categories desde Swagger.

## Resultado esperado:

Devuelve una lista de categorias.
Cada categoria muestra nombre, descripcion y estado.
Si no hay categorias, devuelve una lista vacia.
