# AI Interview Preparation System

A full-stack AI-powered interview preparation system built with Django and FastAPI.

## Architecture

- **Django**: Main backend with authentication, dashboard, and frontend templates
- **FastAPI**: Microservice for AI processing (question generation, answer evaluation)
- **PostgreSQL/SQLite**: Primary database
- **Tailwind CSS**: Modern responsive UI

## Quick Start

### 1. Django Backend

```bash
cd django_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2. FastAPI Service

```bash
cd fastapi_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

### 3. Access the Application

- Django: http://localhost:8000
- FastAPI docs: http://localhost:8001/docs

## Features

- User authentication (signup, login, logout)
- Role-based mock interviews (Backend, Frontend, Data Science, etc.)
- AI-generated interview questions
- Text and voice input for answers
- Real-time answer evaluation
- Performance analytics dashboard
- Detailed feedback and improvement suggestions

## API Endpoints

### Django API
- `POST /api/auth/signup/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/interviews/` - List interviews
- `POST /api/interviews/start/` - Start new interview
- `POST /api/interviews/{id}/submit-answer/` - Submit answer

### FastAPI AI Service
- `POST /ai/generate-questions/` - Generate interview questions
- `POST /ai/evaluate-answer/` - Evaluate answer
- `POST /ai/transcribe/` - Speech-to-text

## Configuration

Copy `.env.example` to `.env` and configure:
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection
- `FASTAPI_URL` - FastAPI service URL

## Technologies Used

- Django 4.2+
- FastAPI
- PostgreSQL
- Hugging Face Transformers
- spaCy
- Whisper
- Tailwind CSS

## License

MIT License
