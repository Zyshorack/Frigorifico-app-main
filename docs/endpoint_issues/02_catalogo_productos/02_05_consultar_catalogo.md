# 2.5 Consultar catalogo disponible

## Objetivo

Implementar el flujo para consultar productos activos con cantidad disponible.
A diferencia de GET /products, este endpoint calcula disponibilidad usando lotes con status active, no vencidos y con cantidad restante.

## Endpoint

GET /catalog

## Archivos involucrados

- app/controller/products.py
- app/dto/products.py
- app/services/product_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el catalogo disponible.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service pide al repository los productos activos.
4. El repository suma lotes con status active, no vencidos y con cantidad restante.
5. Se agrega available_quantity a cada producto.
6. Se devuelve el catalogo calculado.

## Response

Implementar response_model con list[CatalogProductRead] de ser necesario.

## Campos principales:

id
category_id
name
description
unit
available_quantity

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar GET /catalog desde Swagger despues de cargar stock.

## Resultado esperado:

Devuelve productos registrados.
available_quantity refleja solo lotes con status active y no vencidos.
Productos sin stock pueden aparecer con cantidad 0.
