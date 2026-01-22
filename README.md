# AI Job Recommendation System

A modern AI-powered job recommendation system that analyzes resumes and provides personalized job matches with detailed explanations.

![Tech Stack](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python-green)
![AI](https://img.shields.io/badge/AI-Gemini%20%7C%20OpenAI-purple)
![Database](https://img.shields.io/badge/Database-PostgreSQL-orange)

## ✨ Features

- **📄 Resume Upload**: Upload PDF, DOCX, or TXT resumes
- **🧠 AI Analysis**: Extract skills, experience, and role keywords using AI
- **🎯 Smart Matching**: Get personalized job recommendations
- **💬 Detailed Explanations**: Understand why each job matches your profile
- **📊 Match Scores**: See compatibility percentage for each role

## 🏗️ Architecture

```
User (React + TypeScript UI)
        ↓
Backend API (FastAPI + Python)
        ↓
AI API (Gemini / OpenAI)
        ↓
Job Matching Logic
        ↓
Response + Explanation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Gemini API Key or OpenAI API Key

### 1. Clone and Setup

```bash
cd Job_recommendation_web
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and database URL
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb job_recommendation

# Or using psql
psql -c "CREATE DATABASE job_recommendation;"
```

### 4. Configure API Keys

Edit `backend/.env`:

```env
# Choose your AI provider
AI_PROVIDER=gemini  # or 'openai'

# Add your API key
GEMINI_API_KEY=your_gemini_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/job_recommendation
```

### 5. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 6. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 7. Access the App

- Frontend: http://localhost:5173
- Backend API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📁 Project Structure

```
Job_recommendation_web/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Configuration settings
│   │   ├── database.py       # Database connection
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── routers/
│   │   │   ├── users.py      # User endpoints
│   │   │   ├── resume.py     # Resume upload & analysis
│   │   │   └── jobs.py       # Job recommendations
│   │   └── services/
│   │       ├── resume_parser.py  # PDF/DOCX parsing
│   │       └── ai_service.py     # AI integration
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── api/              # API service layer
    │   ├── components/       # React components
    │   │   ├── Header.tsx
    │   │   ├── ResumeUpload.tsx
    │   │   ├── AnalyzingLoader.tsx
    │   │   ├── ResumeCard.tsx
    │   │   ├── JobCard.tsx
    │   │   └── ResultsDashboard.tsx
    │   ├── types/            # TypeScript types
    │   ├── App.tsx           # Main application
    │   └── index.css         # Design system
    └── .env
```

## 🔌 API Endpoints

### Users
- `POST /api/users/` - Create user
- `GET /api/users/{id}` - Get user by ID
- `GET /api/users/email/{email}` - Get user by email

### Resume
- `POST /api/resume/upload` - Upload and analyze resume
- `GET /api/resume/{id}` - Get resume by ID
- `GET /api/resume/user/{email}` - Get user's resumes

### Jobs
- `POST /api/jobs/recommend` - Generate job recommendations
- `GET /api/jobs/recommendations/{email}` - Get user's recommendations

## 🎨 Design System

The frontend uses a modern dark theme with:
- **Glassmorphism** effects
- **Purple/Cyan** gradient accents
- **Smooth animations**
- **Responsive design**

## 🤖 AI Prompts

The system uses carefully crafted prompts for:

1. **Resume Analysis**: Extracts skills, experience, education, and suggests potential roles
2. **Job Matching**: Generates relevant job recommendations with explanations
3. **Skill Gap Analysis**: Identifies matching skills and areas for improvement

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI service to use | `gemini` |
| `GEMINI_API_KEY` | Google Gemini API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `CORS_ORIGINS` | Allowed frontend origins | `localhost:5173` |

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
