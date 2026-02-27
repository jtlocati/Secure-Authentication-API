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

## What I Learned:
Python constructs such as FastAPI relate heavaly to other packages that im already familiar with such as Django and Flask. The File structure of Fast API i saw to have relationships.

| Your FastAPI Project | Django Equivalent                         | Function                  |
| -------------------- | ----------------------------------------- | ------------------------- |
| `main.py`            | `urls.py` + `settings.py` entry           | Application bootstrapping |
| `api/routes/auth.py` | `views.py`                                | HTTP endpoints            |
| `schemas/*.py`       | Django Forms / DRF Serializers            | Input + output validation |
| `models/user.py`     | `models.py`                               | Database table definition |
| `services/users.py`  | Custom service layer (not default Django) | Business logic            |
| `core/security.py`   | `django.contrib.auth`                     | Password + auth logic     |
| `core/deps.py`       | Middleware + request.user                 | Per-request context       |
| Alembic              | `makemigrations` / `migrate`              | Schema migration system   |
| `.env + config.py`   | `settings.py`                             | Configuration management  |
