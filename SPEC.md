# AI Interview Preparation System - Specification

## 1. Project Overview

**Project Name:** AI Interview Preparation System  
**Project Type:** Full-stack Web Application with Microservices Architecture  
**Core Functionality:** An intelligent interview preparation platform that generates role-specific interview questions, evaluates user responses using AI, and provides detailed feedback with performance analytics.  
**Target Users:** Job seekers, students, and professionals preparing for technical interviews

## 2. Architecture

### 2.1 System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Django Templates + Tailwind)    │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Django Backend (Port 8000)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Auth System │  │ Dashboard   │  │ Interview Management    │  │
│  │ (Django Auth)│ │ & Analytics │  │ & Session Handling      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                    REST API (HTTP Requests)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Microservice (Port 8001)               │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │ Question Gen AI │  │ Answer Evaluator │  │ Speech-to-Text  │  │
│  │ (HuggingFace)   │  │ (spaCy + HF)     │  │ (Whisper)      │  │
│  └─────────────────┘  └──────────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Databases                                │
│  ┌──────────────────────┐    ┌───────────────────────────────┐  │
│  │ PostgreSQL           │    │ MongoDB (Optional)            │  │
│  │ - User data          │    │ - Interview responses          │  │
│  │ - Interview history  │    │ - Unstructured feedback       │  │
│  │ - Performance stats  │    │ - Chat logs                   │  │
│  └──────────────────────┘    └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend Framework | Django 4.2+ | Main server, auth, templates |
| AI Microservice | FastAPI | AI processing, async operations |
| Primary Database | PostgreSQL | User data, interviews, analytics |
| Document Store | MongoDB | Interview responses, feedback |
| AI - Question Gen | Hugging Face (GPT-2/FLAN-T5) | Generate interview questions |
| AI - Evaluation | spaCy + Transformers | NLP analysis, keyword extraction |
| AI - Speech-to-Text | Whisper (OpenAI) | Voice input processing |
| Frontend | Tailwind CSS + Alpine.js | Modern responsive UI |
| API Communication | REST (httpx) | Inter-service communication |

## 3. Database Schema

### 3.1 PostgreSQL Models

#### User Model (Extended Django User)
```
users_customuser
├── id: UUID (PK)
├── email: VARCHAR(255) UNIQUE
├── password: VARCHAR(255)
├── first_name: VARCHAR(100)
├── last_name: VARCHAR(100)
├── phone: VARCHAR(20) NULLABLE
├── resume_text: TEXT NULLABLE
├── target_role: VARCHAR(100) NULLABLE
├── experience_level: VARCHAR(20) (junior/mid/senior)
├── created_at: TIMESTAMP
├── updated_at: TIMESTAMP
└── is_active: BOOLEAN
```

#### Interview Model
```
interviews_interview
├── id: UUID (PK)
├── user_id: UUID (FK)
├── role: VARCHAR(100)
├── interview_type: VARCHAR(50) (technical/behavioral/mixed)
├── status: VARCHAR(20) (in_progress/completed/abandoned)
├── started_at: TIMESTAMP
├── completed_at: TIMESTAMP NULLABLE
├── total_questions: INTEGER
├── overall_score: DECIMAL(5,2) NULLABLE
├── technical_score: DECIMAL(5,2) NULLABLE
├── communication_score: DECIMAL(5,2) NULLABLE
├── duration_minutes: INTEGER NULLABLE
└── created_at: TIMESTAMP
```

#### Question Model
```
interviews_question
├── id: UUID (PK)
├── interview_id: UUID (FK)
├── question_text: TEXT
├── question_type: VARCHAR(50)
├── difficulty: VARCHAR(20)
├── order: INTEGER
├── expected_keywords: JSONB
├── created_at: TIMESTAMP
└── time_limit_seconds: INTEGER
```

#### Answer Model
```
interviews_answer
├── id: UUID (PK)
├── question_id: UUID (FK)
├── user_id: UUID (FK)
├── answer_text: TEXT
├── audio_url: VARCHAR(500) NULLABLE
├── is_voice_input: BOOLEAN
├── technical_score: DECIMAL(5,2) NULLABLE
├── communication_score: DECIMAL(5,2) NULLABLE
├── feedback: TEXT NULLABLE
├── missing_points: JSONB NULLABLE
├── keywords_found: JSONB NULLABLE
├── answered_at: TIMESTAMP
└── evaluation_completed_at: TIMESTAMP NULLABLE
```

### 3.2 MongoDB Collections

#### Interview Responses Collection
```javascript
{
  "_id": ObjectId,
  "interview_id": UUID,
  "question_id": UUID,
  "response": {
    "text": String,
    "audio_transcript": String,
    "entities_detected": Array,
    "sentiment": String,
    "language_metrics": Object
  },
  "analysis": {
    "technical_depth": Number,
    "completeness": Number,
    "clarity": Number,
    "relevance": Number
  },
  "improvements": Array,
  "created_at": DateTime
}
```

## 4. API Specifications

### 4.1 Django REST API Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/profile/` | Get user profile |
| PUT | `/api/auth/profile/` | Update user profile |

#### Interviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/interviews/start/` | Start new interview |
| GET | `/api/interviews/` | List user's interviews |
| GET | `/api/interviews/{id}/` | Get interview details |
| POST | `/api/interviews/{id}/submit-answer/` | Submit answer |
| POST | `/api/interviews/{id}/complete/` | Complete interview |
| GET | `/api/interviews/{id}/results/` | Get interview results |

#### Questions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/interviews/{id}/questions/` | Get questions for interview |
| GET | `/api/interviews/{id}/questions/{q_id}/` | Get specific question |

#### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/summary/` | Get overall analytics |
| GET | `/api/analytics/performance/` | Get performance trends |
| GET | `/api/analytics/role-analysis/` | Get role-specific analysis |

### 4.2 FastAPI Internal API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/generate-questions/` | Generate interview questions |
| POST | `/ai/evaluate-answer/` | Evaluate user answer |
| POST | `/ai/transcribe/` | Transcribe audio |
| GET | `/health/` | Health check |

## 5. UI/UX Specification

### 5.1 Color Palette

| Color | Hex Code | Usage |
|-------|----------|-------|
| Primary | `#2563EB` | Buttons, links, accents |
| Primary Dark | `#1D4ED8` | Button hover states |
| Secondary | `#10B981` | Success states, positive scores |
| Warning | `#F59E0B` | Warnings, medium scores |
| Danger | `#EF4444` | Errors, low scores |
| Background | `#F8FAFC` | Page backgrounds |
| Surface | `#FFFFFF` | Cards, panels |
| Text Primary | `#1E293B` | Main text |
| Text Secondary | `#64748B` | Secondary text |
| Border | `#E2E8F0` | Borders, dividers |

### 5.2 Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Headings | Inter | 24-36px | 700 |
| Body | Inter | 14-16px | 400 |
| Labels | Inter | 12-14px | 500 |
| Code | JetBrains Mono | 14px | 400 |

### 5.3 Spacing System

- Base unit: 4px
- Margins: 16px, 24px, 32px
- Padding: 8px, 12px, 16px, 24px
- Border radius: 8px (cards), 6px (buttons), 4px (inputs)

### 5.4 Page Specifications

#### Landing Page
- Hero section with gradient background (#2563EB to #1D4ED8)
- Features grid (3 columns on desktop)
- Call-to-action buttons
- Testimonial carousel

#### Authentication Pages
- Centered card layout
- Form with floating labels
- Social login buttons (optional)
- Password strength indicator

#### Dashboard
- Sidebar navigation (collapsible)
- Top bar with user menu
- Stats cards grid (4 columns)
- Recent interviews table
- Performance charts (Line/Area)

#### Interview Interface
- Full-screen mode option
- Question card with timer
- Answer input area (text + voice)
- Progress indicator
- Skip/Hint buttons
- Real-time feedback display

#### Results Page
- Overall score gauge
- Score breakdown cards
- Question-by-question review
- Feedback and recommendations
- Share/Download options

## 6. Functional Requirements

### 6.1 Authentication Flow
1. User signs up with email/password
2. Email verification (optional)
3. Login redirects to dashboard
4. Session-based authentication with Django
5. Protected routes require authentication

### 6.2 Interview Flow
1. User selects role and interview type
2. System generates questions via FastAPI
3. Questions presented one at a time
4. User types or speaks answer
5. Answer submitted for AI evaluation
6. Immediate feedback displayed
7. Repeat until all questions answered
8. Final results and analytics shown

### 6.3 AI Question Generation
- Role-specific question banks
- Difficulty adjustment based on experience
- Mix of technical and behavioral questions
- Time limits per question
- Follow-up question generation

### 6.4 AI Answer Evaluation
- Keyword matching against expected keywords
- NLP analysis for completeness
- Communication skills assessment
- Code snippet detection (for technical)
- Structured scoring rubric

### 6.5 Speech-to-Text
- Browser MediaRecorder API
- Audio sent to FastAPI Whisper endpoint
- Transcript returned and displayed
- Manual correction option

### 6.6 Analytics Dashboard
- Total interviews completed
- Average scores over time
- Strongest/weakest areas
- Role-specific performance
- Improvement recommendations

## 7. Security Requirements

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS prevention (template escaping)
- Rate limiting on API endpoints
- Secure password hashing (PBKDF2)
- Session security (httpOnly cookies)
- CORS configuration for API

## 8. Error Handling

- Custom exception handlers
- User-friendly error messages
- Error logging and monitoring
- Graceful degradation for AI failures
- Retry mechanisms for API calls
- Fallback responses for AI unavailability

## 9. Project Structure

```
ai-interview-system/
├── django_backend/                 # Django project
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/                    # Django settings
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                     # User management app
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── admin.py
│   ├── interviews/                # Interview app
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── admin.py
│   ├── analytics/                 # Analytics app
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── api/                       # REST API
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── serializers.py
│   └── templates/                 # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── dashboard.html
│       ├── auth/
│       │   ├── login.html
│       │   └── signup.html
│       ├── interview/
│       │   ├── start.html
│       │   ├── session.html
│       │   └── results.html
│       └── analytics/
│           └── performance.html
├── fastapi_service/              # FastAPI microservice
│   ├── main.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── question_generator.py
│   │   │   ├── answer_evaluator.py
│   │   │   └── speech_to_text.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── ai.py
│   │   │   └── health.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── nlp.py
│   └── models/                    # AI models cache
├── static/                       # Static files
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── app.js
│       ├── interview.js
│       └── analytics.js
├── media/                        # User uploads
├── tests/                        # Test files
├── .env.example
├── docker-compose.yml
└── README.md
```

## 10. Acceptance Criteria

### Authentication
- [ ] User can sign up with email and password
- [ ] User can login and logout
- [ ] Protected pages redirect to login
- [ ] Password is securely hashed

### Interview System
- [ ] User can start interview for specific role
- [ ] Questions are generated based on role
- [ ] User can answer questions via text
- [ ] User can answer questions via voice (optional)
- [ ] Answers are evaluated with scores
- [ ] Feedback is provided for each answer
- [ ] Interview can be completed

### Dashboard
- [ ] Dashboard shows interview history
- [ ] Analytics charts display correctly
- [ ] Performance metrics are accurate
- [ ] Navigation is intuitive

### AI Integration
- [ ] Questions are contextually relevant
- [ ] Evaluation provides meaningful feedback
- [ ] Speech transcription works (if implemented)
- [ ] System handles AI service failures gracefully

### Performance
- [ ] Pages load within 2 seconds
- [ ] AI responses within 10 seconds
- [ ] System handles concurrent users
- [ ] Database queries are optimized

## 11. Configuration

### Environment Variables
```
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ai_interview_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# FastAPI
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8001
AI_MODEL_NAME=facebook/bart-large-cnn

# Hugging Face
HF_API_TOKEN=your-hf-token

# MongoDB (Optional)
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=interview_responses
```

## 12. Deployment Notes

- Use Docker for containerization
- Set up Nginx as reverse proxy
- Configure PostgreSQL with connection pooling
- Enable HTTPS in production
- Set up automated backups
- Monitor with logging services
