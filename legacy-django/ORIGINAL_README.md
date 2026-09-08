# LearnSphere

LearnSphere is a full-stack learning and study-collaboration platform built with Python and Django. It combines two experiences in one app: real-time topic-based study rooms where learners can discuss and chat, and a structured online course system with lessons, quizzes, progress tracking, and instructor tools. A Django REST Framework API is included so the same data can power a mobile app or a separate JavaScript frontend.

## Tech Stack

This project follows the same core stack used in the referenced Python full-stack developer tutorial, with additional tools layered on top for the new features:

**Backend**
- Python 3
- Django 5 (MVT architecture, ORM, authentication, admin panel)
- Django REST Framework (REST API, serializers, viewsets, routers)
- SQLite (default development database)
- django-filter (API filtering)
- django-cors-headers (cross-origin API access)
- Whitenoise (static file serving in production)
- Pillow (image uploads for avatars, thumbnails)

**Frontend**
- HTML5
- CSS3 (custom responsive styling, no external UI framework)
- Vanilla JavaScript (DOM interactions, theme toggle, alert dismissal)
- Django Template Language

**Other**
- Token authentication (DRF)
- Django's built-in email backend (console backend for development, SMTP for production)
- python-decouple / environment variables for configuration
- Gunicorn (production WSGI server)

## Core Features

- User registration, login, and logout
- Create, read, update, and delete study rooms
- Topic-based organization of rooms
- Search rooms by topic, name, or description
- Threaded chat messages inside each room
- Join a room automatically by posting a message
- Restricted access so only the host can edit or delete their room
- User profile pages showing hosted rooms and recent messages
- Site-wide activity feed of recent messages
- Static file handling and a custom theme

## New Features Added on Top

- **Custom user model** with avatar, headline, bio, and a points/reputation system
- **Follow system** between users, with follower/following counts on profiles
- **Leaderboard** ranking users by points earned from activity
- **Tags** for study rooms (comma-separated input, tag cloud, filter by tag)
- **Likes and bookmarks** for study rooms, with a dedicated "My Bookmarks" page
- **Pinned rooms** and **scheduled/live session** timestamps for rooms
- **Threaded replies** to chat messages (reply-to-message support)
- **Email verification** on signup and **password reset** flow (Django auth views)
- **Notifications system** that reacts to follows, likes, replies, and course enrollments, with an unread-count badge in the navbar
- **Full online course module**: categories, courses, lessons, video embeds, and instructor-created content
- **Enrollment and progress tracking**, including per-lesson completion and automatic course-completion detection
- **Quizzes** attached to lessons with multiple-choice questions, scoring, pass/fail thresholds, and points rewarded for passing
- **Course reviews and ratings** (1–5 stars) with average rating calculation
- **Search, category, and level filters** for the course catalog, with pagination
- **REST API** covering rooms, topics, tags, messages, courses, lessons, and categories, including a custom `toggle_like` API action and token authentication endpoint
- **Dark theme UI** with a light-mode toggle persisted via local storage

## Project Structure

```
learnsphere/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── learnsphere/            # Project settings, root URLs, WSGI/ASGI
├── users/                  # Custom user model, auth, follows, leaderboard
├── study/                  # Study rooms, topics, tags, messages, bookmarks
├── courses/                # Courses, lessons, enrollments, quizzes, reviews
├── notifications/          # Notification model, signals, context processor
├── api/                    # DRF serializers, viewsets, routers
├── templates/              # All HTML templates (base, rooms, courses, quiz, auth)
└── static/
    ├── css/main.css
    └── js/main.js
```

## Setup Instructions

1. **Clone and enter the project**
   ```
   git clone <your-repo-url>
   cd learnsphere
   ```

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```
   cp .env.example .env
   ```
   Update `SECRET_KEY` and email settings as needed.

5. **Run migrations**
   ```
   python manage.py migrate
   ```

6. **Create a superuser**
   ```
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```
   python manage.py runserver
   ```

8. Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for the admin panel.

## API Endpoints

All endpoints are available under `/api/`:

| Endpoint | Description |
|---|---|
| `/api/rooms/` | List, create, retrieve, update, delete study rooms |
| `/api/rooms/{id}/toggle_like/` | Like/unlike a room (POST) |
| `/api/topics/` | List topics |
| `/api/tags/` | List tags |
| `/api/messages/` | List/create chat messages |
| `/api/courses/` | List, create, retrieve, update, delete courses |
| `/api/lessons/` | List/create lessons |
| `/api/categories/` | List course categories |
| `/api/token-auth/` | Obtain an auth token (POST username/password) |

## Notes

- Media files (avatars, thumbnails) are stored under `media/` and served locally in development.
- The default avatar is an inline SVG placeholder located at `media/avatars/default.svg`.
- Notifications are generated automatically through Django signals when a follow, like, reply, or enrollment occurs — no manual triggering needed.
- Switch `DEBUG=False` and configure `ALLOWED_HOSTS`, a production database, and a real email backend before deploying.

## License

This project is provided for educational and portfolio purposes.
