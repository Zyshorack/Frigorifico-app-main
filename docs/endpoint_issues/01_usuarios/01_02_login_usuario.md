# 1.2 Login de usuario

## Objetivo

Implementar el flujo para iniciar sesion con un usuario existente.
El login valida que el usuario exista, esta activo y que la contrasena enviada coincida con la contrasena guardada como hash.

## Endpoint

POST /users/login

## Archivos involucrados

- app/controller/users.py
- app/dto/users.py
- app/services/user_service.py
- app/models/domain.py
- app/core/security.py

## Trabajo a realizar

Completar los TODOs relacionados con el login de usuarios.

El flujo esperado es:

1. El controller recibe username y password.
2. El controller llama al service.
3. El service busca un usuario activo por username.
4. Si no existe, responde HTTP 401 Unauthorized.
5. Si existe, compara la contrasena enviada contra el hash guardado.
6. Si no coincide, responde HTTP 401 Unauthorized.
7. Si coincide, devuelve los datos publicos del usuario.

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

Probar POST /users/login desde Swagger.

## Resultado esperado:

Un usuario valido puede iniciar sesion.
Credenciales incorrectas responden HTTP 401.
La response no expone password_hash.

### Request

```json
{
  "username": "admin",
  "password": "admin123"
}
```
