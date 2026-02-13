# Secure Auth API (FastAPI)

A production-style FastAPI REST API that implements secure user authentication and authorization with JWTs, role-based access control, rate limiting, and a PostgreSQL-backed data layer with migrations. The goal is to provide a clean, hire-ready backend foundation that demonstrates real-world security and engineering practices.

## Features
- User registration and login
- Password hashing
- JWT authentication
- Role-based access control (user/admin)
- Protected routes
- Basic rate limiting
- PostgreSQL + SQLAlchemy + Alembic migrations
- Tests (pytest)
- Docker + docker-compose
- OpenAPI docs via FastAPI

## Tech Stack
FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, passlib/bcrypt, python-jose, pytest, Docker
