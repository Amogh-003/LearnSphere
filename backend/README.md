# LearnSphere Backend (FastAPI)

REST API for the LearnSphere learning & study-collaboration platform.

## Tech Stack

- **FastAPI** – modern, high-performance async web framework
- **SQLAlchemy 2.0** (async) + **aiosqlite** (dev) / PostgreSQL (prod)
- **Pydantic v2** – validation & serialization
- **JWT** (python-jose) + **passlib[bcrypt]** – authentication
- **Alembic** – database migrations (optional)

## Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

- API docs (Swagger): http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Obtain JWT access token |
| GET | `/api/auth/me` | Current user profile |
| GET | `/api/rooms/` | List / search study rooms |
| POST | `/api/rooms/` | Create a room |
| GET | `/api/rooms/{id}` | Room detail |
| POST | `/api/rooms/{id}/toggle_like` | Like / unlike |
| GET/POST | `/api/rooms/{id}/messages` | Chat messages |
| GET | `/api/courses/` | List published courses |
| POST | `/api/courses/` | Create a course |
| POST | `/api/courses/{id}/enroll` | Enroll in a course |
| GET | `/api/courses/{id}/lessons` | List lessons |
| POST | `/api/courses/{id}/reviews` | Add a review |

## Project Structure

```
backend/
├── app/
│   ├── api/          # Route handlers
│   ├── core/         # Config, DB, security
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── main.py
├── requirements.txt
└── .env.example
```
