# 1 - Objetivo

`Frigorifico API` es una API educativa para administrar operaciones basicas de un frigorifico o camara de frio.

El objetivo es practicar backend con FastAPI usando un dominio concreto:

- usuarios del sistema;
- categorias y productos;
- camaras o zonas de frio;
- sensores y lecturas;
- alertas operativas;
- evidencia de acciones correctivas;
- lotes de mercaderia;
- entradas y salidas de stock usando FIFO.

## Enfoque del MVP

El sistema prioriza tres ideas:

1. Control de frio: registrar camaras, sensores y lecturas.
2. Evidencia operativa: toda alerta resuelta debe tener una accion correctiva.
3. Trazabilidad de stock: cada entrada o salida queda registrada como movimiento.

## Para que sirve como proyecto de aprendizaje

Sirve para aprender a separar responsabilidades:

- el controller recibe requests HTTP;
- el DTO valida datos de entrada y salida;
- el service aplica reglas de negocio;
- el repository concentra consultas reutilizables;
- el model representa las tablas de la base.

## Alcance actual

El proyecto no busca ser un ERP completo ni un ecommerce.

Quedan como mejoras futuras:

- permisos reales por rol en backend;
- autenticacion con JWT;
- migraciones con Alembic;
- reportes operativos;
- alertas automaticas de vencimiento y stock bajo;
- base PostgreSQL o MySQL para despliegues reales.
