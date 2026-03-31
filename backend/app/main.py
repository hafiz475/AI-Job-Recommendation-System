"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.routers import users, resume, jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🚀 Starting AI Job Recommendation System...")
    init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI application
app = FastAPI(
    title="AI Job Recommendation System",
    description="""
    An intelligent job recommendation system that analyzes resumes using AI 
    and provides personalized job matches with detailed explanations.
    
    ## Features
    
    * **Resume Upload**: Upload PDF, DOCX, or TXT resumes
    * **AI Analysis**: Extract skills, experience, and role keywords
    * **Smart Matching**: Get AI-powered job recommendations
    * **Detailed Explanations**: Understand why each job matches your profile
    
    ## API Endpoints
    
    * `/api/users` - User management
    * `/api/resume` - Resume upload and analysis
    * `/api/jobs` - Job recommendations
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost:5173",  # Local development
    "http://localhost:3000",  # Alternative local
    "https://ai-job-recommendation-system-omega.vercel.app",  # Vercel frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api")
app.include_router(resume.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to AI Job Recommendation System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "ai_provider": settings.ai_provider,
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
