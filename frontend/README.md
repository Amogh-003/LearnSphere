# LearnSphere Frontend (Next.js)

Modern React frontend for the LearnSphere learning platform.

## Tech Stack

- **Next.js 14** (App Router)
- **React 18** + TypeScript
- **Tailwind CSS** – utility-first styling with dark theme
- **Axios** – HTTP client
- **js-cookie** – JWT token storage
- **Lucide React** – icons

## Quick Start

```bash
cd frontend
cp .env.example .env.local
# Edit NEXT_PUBLIC_API_URL if backend runs elsewhere
npm install
npm run dev
```

Open http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/           # App Router pages
│   │   ├── page.tsx          # Home
│   │   ├── rooms/            # Study rooms
│   │   ├── courses/          # Courses catalog
│   │   └── login/            # Auth
│   ├── components/    # Shared UI
│   ├── lib/           # API client, helpers
│   ├── types/         # TypeScript interfaces
│   └── hooks/         # Custom React hooks
├── public/
└── package.json
```

## Environment

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | FastAPI base URL | `http://127.0.0.1:8000/api` |
