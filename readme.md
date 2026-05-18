# 📦 Project Setup Documentation

This project uses Docker Compose to run a FastAPI-based web service along with a PostgreSQL database.

## 🚀 Prerequisites

Before running the project, ensure you have:

- Docker installed: https://docs.docker.com/get-docker/
- Docker Compose installed: https://docs.docker.com/compose/install/

---

## 🐳 Services Overview

The application consists of two main services:

### 1. Database Service (`db`)

Uses PostgreSQL 15.

Features:

- Stores application data
- Persists data using Docker volumes
- Includes health checks to ensure readiness before the API starts

### 2. Web Service (`web`)

FastAPI application served using Uvicorn.

Features:

- Connects to PostgreSQL database
- Runs in development mode with auto-reload
- Syncs local code into the container for live updates

---

## 📄 Docker Compose Configuration

```yaml
services:
  db:
    image: postgres:15
    container_name: book-library-db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - ${DB_PORT_FROM}:${DB_PORT_TO}
    volumes:
      - ${DATABASE_PATH}:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    image: <image_name>
    container_name: book-library-api
    command: uvicorn main:app --host ${API_HOST} --port ${API_PORT} --reload
    ports:
      - ${API_PORT_FROM}:${API_PORT}
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:${DB_PORT_TO}/${POSTGRES_DB}
    depends_on:
      db:
        condition: service_healthy
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

### 🗄️ Database Configuration

| Variable | Description |
|-----------|-------------|
| `POSTGRES_USER` | Username for PostgreSQL |
| `POSTGRES_PASSWORD` | Password for PostgreSQL |
| `POSTGRES_DB` | Database name |
| `DB_HOST` | Database host (usually `db` in Docker) |
| `DB_PORT_FROM` | Host port for database (e.g., `5432`) |
| `DB_PORT_TO` | Container port for database (usually `5432`) |

### 🌐 API Configuration

| Variable | Description |
|-----------|-------------|
| `API_HOST` | Host for FastAPI (e.g., `0.0.0.0`) |
| `API_PORT_FROM` | Host machine port (e.g., `8000`) |
| `API_PORT` | Container port for FastAPI |
| `RELOAD` | Enable auto-reload (`true` for development) |

### 🔗 URLs

| Variable | Description |
|-----------|-------------|
| `DATABASE_URL` | Full database connection string (optional if generated in Compose) |

Example:

```env
DATABASE_URL=postgresql://user:password@db:5432/dbname
```

### 📦 Docker Volumes

| Variable | Description |
|-----------|-------------|
| `DATABASE_PATH` | Path where PostgreSQL data is stored (e.g., `/var/lib/postgresql/data`) |

---

## ▶️ How to Run the Project

### 1. Create `.env` file

Fill in all required environment variables.

### 2. Build and start containers

```bash
docker-compose up --build
```

### 3. Access the application

**API:**

```text
http://localhost:API_PORT_FROM
```

**Database:**

Runs internally through the Docker network using the `db` service.

---

## 🧠 Important Notes

- The web service waits for the database to become healthy before starting.
- Data is persisted using Docker volumes.
- Code changes are reflected instantly through volume mounting (`.:/app`) during development.

---

## 🧹 Stop the Project

Stop containers:

```bash
docker-compose down
```

Remove containers and volumes:

```bash
docker-compose down -v
```