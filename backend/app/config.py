"""Application configuration settings."""
from typing import Optional, List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Database - defaults to SQLite for easy development
        # Change to PostgreSQL for production: postgresql://user:pass@localhost/db
        self.database_url: str = os.getenv(
            "DATABASE_URL", 
            "sqlite:///./job_recommendation.db"
        )
        
        # AI Configuration
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.ai_provider: str = os.getenv("AI_PROVIDER", "gemini")
        
        # Server
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.debug: bool = os.getenv("DEBUG", "True").lower() == "true"
        
        # CORS
        cors_string = os.getenv(
            "CORS_ORIGINS", 
            "http://localhost:5173,http://localhost:3000"
        )
        self.cors_origins: List[str] = [origin.strip() for origin in cors_string.split(",")]


settings = Settings()
