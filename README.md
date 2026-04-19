# User API

Production-style REST API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker, JWT authentication and Pytest.

## Features

- User CRUD operations
- User registration and login
- JWT-based authentication
- PostgreSQL database integration
- SQLAlchemy ORM models
- Alembic database migrations
- Dockerized local environment
- Pytest API tests
- Interactive Swagger documentation

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker / Docker Compose
- Pytest
- JWT

## Run with Docker

```bash
docker-compose up --build
```

## Run locally

```bash
python3 -m uvicorn main:app --reload --port 8001
```

## Database migrations

```bash
alembic upgrade head
```

## Run tests

```bash
pytest
```

## API Documentation

After starting the app, open:

```text
http://localhost:8001/docs
```

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /users | Create user |
| GET | /users | Get all users |
| GET | /users/{user_id} | Get user by ID |
| PUT | /users/{user_id} | Update user |
| DELETE | /users/{user_id} | Delete user |
| POST | /login | Login and receive JWT token |

## Project Goal

This project demonstrates backend development skills with FastAPI, database modeling, migrations, authentication, Docker-based setup and automated testing.
