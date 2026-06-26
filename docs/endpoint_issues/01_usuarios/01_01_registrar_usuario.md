# 1.1 Registrar usuario

## Objetivo

Implementar el flujo para registrar un usuario del sistema.
El usuario permite identificar quien opera el sistema y que rol tiene dentro de la aplicacion.
Roles disponibles:
- admin
- operator
- client

## Endpoint

POST /users

## Archivos involucrados

- app/controller/users.py
- app/dto/users.py
- app/services/user_service.py
- app/repositories/domain_repository.py
- app/models/domain.py

## Trabajo a realizar

Completar los TODOs relacionados con la creacion de usuarios.

El flujo esperado es:

1. El controller recibe la request.
2. El controller llama al service.
3. El service valida si ya existe un usuario con el mismo username.
4. Si ya existe, responde HTTP 409 Conflict.
5. Si no existe, genera el hash de la contrasena.
6. Crea el usuario.
7. Devuelve el usuario creado sin exponer password_hash.

## Response

Implementar response_model con UserRead de ser necesario.

## Campos principales:

id
username
role

## Notas

- Mantener la logica de negocio fuera del controller.
- Utilizar HTTPException para errores esperados.
- Revisar implementaciones similares dentro del proyecto.

## Prueba manual sugerida

Probar POST /users desde Swagger.

## Resultado esperado:

Se crea un usuario valido.
Si ya existe un usuario con el mismo username, responde HTTP 409.
La contrasena no se devuelve en la response.

### Request

```json
{
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}
```
