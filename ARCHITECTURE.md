# Architecture

## Auth Flow
1. POST /auth/register -> create user (hashed password)
2. POST /auth/login -> verify password -> return JWT
3. Requests to protected routes include Authorization: Bearer <token>
4. Dependency decodes JWT -> loads user -> enforces role if needed

## Roles
- user: default
- admin: elevated access to admin-only endpoints

## Modules
- app/api/routes: HTTP endpoints (thin)
- app/services: business logic
- app/models: SQLAlchemy ORM models
- app/schemas: Pydantic request/response models
- app/core: config, security utilities, auth dependencies
- app/db: engine/session/base
- app/middleware: rate limiting
