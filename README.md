# LearnSphere

**LearnSphere** is a full-stack learning and study-collaboration platform.  
It combines real-time topic-based study rooms (chat, likes, tags, participants) with a structured online course system (lessons, quizzes, enrollments, reviews, progress tracking).

> This repository has been updated to a modern tech stack:  
> **Frontend → Next.js (React)** · **Backend → FastAPI (REST APIs)**

The original Django implementation is preserved under `legacy-django/` for reference.

---

## Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** – high-performance async REST API
- **SQLAlchemy 2.0** (async) + SQLite (dev) / PostgreSQL (prod)
- **Pydantic v2** – request/response validation
- **JWT** authentication (python-jose + passlib)
- **CORS** ready for the Next.js frontend

### Frontend
- **Next.js 14** (App Router)
- **React 18** + **TypeScript**
- **Tailwind CSS** – dark-themed responsive UI
- **Axios** + JWT cookies for API calls
- **Lucide React** icons

---

## Project Structure

```
Learn-Sphere/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/             # Auth, rooms, courses routers
│   │   ├── core/            # Config, DB, security
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                # Next.js application
│   ├── src/
│   │   ├── app/             # Pages (home, rooms, courses, login)
│   │   ├── components/
│   │   ├── lib/             # API client
│   │   └── types/
│   ├── package.json
│   └── .env.example
│
├── legacy-django/           # Original Django + DRF project (reference)
└── README.md
```

---

## Features

### Study Rooms
- Create / search / join topic-based rooms
- Threaded chat messages
- Likes, tags, pinned rooms, participant limits
- Auto-join on first message

### Courses
- Instructor-created courses with categories & difficulty levels
- Lessons (text + video embeds)
- Enrollment & progress tracking
- Reviews & ratings (1–5 stars)
- Quizzes (multiple-choice) with pass thresholds & points

### Users
- Registration / login with JWT
- Profiles, points / reputation system
- Follow system & leaderboard (backend models ready)

---

## Getting Started

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger docs → http://127.0.0.1:8000/docs  
- Health check → http://127.0.0.1:8000/health

### 2. Frontend (Next.js)

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

- App → http://localhost:3000

Make sure the backend is running so the frontend can talk to `http://127.0.0.1:8000/api`.

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | Register |
| `POST` | `/api/auth/login` | Login → JWT |
| `GET`  | `/api/auth/me` | Current user |
| `GET`  | `/api/rooms/` | List / search rooms |
| `POST` | `/api/rooms/` | Create room |
| `GET`  | `/api/rooms/{id}` | Room detail |
| `POST` | `/api/rooms/{id}/toggle_like` | Like / unlike |
| `GET`/`POST` | `/api/rooms/{id}/messages` | Chat |
| `GET`  | `/api/courses/` | List published courses |
| `POST` | `/api/courses/` | Create course |
| `POST` | `/api/courses/{id}/enroll` | Enroll |
| `GET`  | `/api/courses/{id}/lessons` | Lessons |
| `POST` | `/api/courses/{id}/reviews` | Add review |

Full interactive documentation is available at `/docs` when the backend is running.

---

## Environment Variables

**Backend** (`.env`)
```
SECRET_KEY=...
DATABASE_URL=sqlite+aiosqlite:///./learnsphere.db
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

**Frontend** (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

---

## Legacy Django Version

The original full-stack Django + Django REST Framework implementation (templates, MVT, etc.) lives in `legacy-django/`.  
You can still run it for comparison or migration reference:

```bash
cd legacy-django
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## License

This project is provided for educational and portfolio purposes.

---

**Happy learning!** ◎
