# 2312284 — DevOps Project

> A production-ready containerized **FastAPI** microservice with a fully automated CI/CD pipeline deployed to **AWS EC2**.

**Student:** Khushi Kandhani · **Reg. No:** 2312284 · **Course:** DevOps Fundamentals — Final Project

---

# Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI + Uvicorn |
| Database | PostgreSQL 15 |
| Containerisation | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 |

---

## Architecture

```
Client (Port 8000)
      │
      ▼
┌─────────────────────────────┐
│  FastAPI + Uvicorn          │  ← Multi-stage Docker build
│  Non-root security context  │    Lightweight production image
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  PostgreSQL 15              │  ← Persistent named volume
│  Port 5432                  │    Data survives restarts
└─────────────────────────────┘

GitHub Actions Pipeline
─────────────────────────────────────────────────────
 push / PR  →  flake8 (lint)  →  pytest (test)
 push main  →  SSH into EC2   →  docker compose up
```

---

## Project Structure

```
2312284-devops-project/
├── .github/workflows/
│   ├── ci.yml                  # Lint (flake8) + Test (pytest)
│   └── cd.yml                  # Auto-deploy to AWS EC2
├── app/
│   ├── main.py                 # FastAPI routes & health checks
│   ├── database.py             # SQLAlchemy engine & sessions
│   ├── models.py               # Student schema (declarative)
│   └── tests/
│       ├── conftest.py         # Fixtures & isolated test DB
│       ├── test_health.py      # /health endpoint tests
│       └── test_students.py    # /students CRUD tests
├── Dockerfile                  # Multi-stage production build
├── docker-compose.yml          # Local development
├── docker-compose.prod.yml     # Production (EC2)
├── .env.example
└── requirements.txt
```

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/students` | List all students |
| `POST` | `/students` | Create a student |
| `GET` | `/students/{id}` | Get student by ID |
| `PUT` | `/students/{id}` | Update a student |
| `DELETE` | `/students/{id}` | Delete a student |

Interactive docs available at `/docs` (Swagger) and `/redoc`.

---

## Local Development

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/Khushi-Kandhani/2312284-devops-project.git
cd 2312284-devops-project

cp .env.example .env        # Fill in your values

docker compose up --build   # API live at http://localhost:8000
```

```bash
docker compose down         # Stop containers
docker compose down -v      # Stop + wipe database volume
```

---

## Environment Variables

Copy `.env.example` to `.env` before running locally.

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_USER` | Database username | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `secret` |
| `POSTGRES_DB` | Database name | `students_db` |
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql://postgres:secret@db:5432/students_db` |

> **Never commit `.env`** — it is already in `.gitignore`.

---

## Running Tests

```bash
# Inside Docker
docker compose run --rm app pytest app/tests/ -v

# Locally (tests use an isolated SQLite DB, no Postgres needed)
pip install -r requirements.txt
pytest app/tests/ -v
```

---

## CI/CD Pipeline

### CI — runs on every push and pull request

1. **Lint** — `flake8` checks PEP 8 compliance
2. **Test** — `pytest` runs the full test suite against an isolated database

Both jobs must pass before a branch can be merged.

### CD — runs on push to `main` only

1. Opens an SSH connection to the AWS EC2 instance
2. Pulls the latest code from `main`
3. Rebuilds and restarts the stack: `docker compose -f docker-compose.prod.yml up -d --build`

**Required GitHub Secrets:**

| Secret | Description |
|--------|-------------|
| `EC2_HOST` | EC2 public IP or DNS |
| `EC2_USER` | SSH username (e.g. `ubuntu`) |
| `EC2_SSH_KEY` | Private key for EC2 access |
| `POSTGRES_USER` | Production DB username |
| `POSTGRES_PASSWORD` | Production DB password |
| `POSTGRES_DB` | Production database name |

---

*2312284 · Khushi Kandhani · DevOps Fundamentals Final Project*
