# 1.3 Listar usuarios

## Objetivo

Implementar el flujo para consultar los usuarios registrados.
Este endpoint sirve para revisar que usuarios existen y que rol tiene cada uno.

## Endpoint

GET /users

## Archivos involucrados

- app/controller/users.py
- app/dto/users.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con el listado de usuarios.

El flujo esperado es:

1. El controller recibe la request.
2. El controller obtiene la sesion de base de datos.
3. Se consulta la tabla users usando el repository.
4. Se devuelve una lista de usuarios.
5. La response no debe incluir password_hash.

## Response

Implementar response_model con list[UserRead] de ser necesario.

## Campos principales:

id
username
role

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar GET /users desde Swagger.

## Resultado esperado:

Devuelve una lista de usuarios registrados.
Cada usuario muestra datos publicos.
No se muestra la contrasena ni el hash.
