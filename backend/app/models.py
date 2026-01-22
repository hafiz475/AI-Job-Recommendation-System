"""Database models for the job recommendation system."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for storing user information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_matches = relationship("JobMatch", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    """Resume model for storing parsed resume data."""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=True)
    
    # AI-extracted data
    skills = Column(JSON, default=list)  # List of skills
    experience = Column(JSON, default=list)  # List of experience entries
    education = Column(JSON, default=list)  # List of education entries
    role_keywords = Column(JSON, default=list)  # Extracted role keywords
    summary = Column(Text, nullable=True)  # AI-generated summary
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    job_matches = relationship("JobMatch", back_populates="resume", cascade="all, delete-orphan")


class Job(Base):
    """Job model for storing job listings."""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default=list)  # Required skills
    experience_level = Column(String(50), nullable=True)  # Entry, Mid, Senior
    salary_range = Column(String(100), nullable=True)
    job_type = Column(String(50), nullable=True)  # Full-time, Part-time, Remote
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job_matches = relationship("JobMatch", back_populates="job")


class JobMatch(Base):
    """Job match model for storing AI-generated job recommendations."""
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)  # Nullable for mock jobs
    
    # Match details
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=True)
    match_score = Column(Integer, default=0)  # 0-100 percentage
    
    # AI explanation
    explanation = Column(Text, nullable=True)  # Why this job matches
    matching_skills = Column(JSON, default=list)  # Skills that match
    missing_skills = Column(JSON, default=list)  # Skills to develop
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="job_matches")
    resume = relationship("Resume", back_populates="job_matches")
    job = relationship("Job", back_populates="job_matches")
