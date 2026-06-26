# 3 - Entidades del sistema

El dominio se divide en usuarios, productos, frio, alertas y stock.

## Usuarios

- `users`: usuarios que operan el sistema.

Un usuario tiene username, password hasheada, rol, estado activo y fecha de creacion.

Roles usados:

- `admin`
- `operator`
- `client`

## Productos

- `product_categories`: categorias de productos.
- `products`: productos que pueden tener stock.

Un producto puede estar asociado a una categoria y usa una unidad, por ejemplo `kg`.

## Frio y sensores

- `cold_locations`: camaras, freezers, heladeras o zonas de frio.
- `sensor_devices`: sensores asociados a una camara o zona.
- `sensor_readings`: lecturas historicas de temperatura y humedad.

Las camaras y sensores pueden definir rangos minimos y maximos. Si una lectura queda fuera de rango, el backend crea una alerta.

## Alertas

- `alerts`: alertas operativas.
Una alerta puede estar abierta, reconocida o resuelta. En esta version simple solo guarda estado y fecha de resolucion.

## Stock

- `batches`: lotes de mercaderia.
- `stock_movements`: movimientos de entrada, salida, ajuste, transferencia o descarte.

Una entrada crea un lote. Una salida consume lotes activos y no vencidos usando FIFO.

## Decisiones de dominio

- El stock real se calcula desde lotes activos no vencidos.
- La salida FIFO no la decide el frontend; vive en backend.
- Los lotes vencidos no se usan para salidas normales.
- Resolver una alerta carga la fecha de resolucion.
- Los movimientos de stock dejan trazabilidad operativa.
