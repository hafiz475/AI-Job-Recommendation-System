"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# ==================== User Schemas ====================

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    name: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Resume Schemas ====================

class ExperienceItem(BaseModel):
    """Schema for experience entry."""
    title: str
    company: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None


class EducationItem(BaseModel):
    """Schema for education entry."""
    degree: str
    institution: Optional[str] = None
    year: Optional[str] = None


class ResumeAnalysis(BaseModel):
    """Schema for AI-analyzed resume data."""
    skills: List[str]
    experience: List[ExperienceItem]
    education: List[EducationItem]
    role_keywords: List[str]
    summary: str


class ResumeResponse(BaseModel):
    """Schema for resume response."""
    id: int
    filename: str
    skills: List[str]
    experience: List[dict]
    education: List[dict]
    role_keywords: List[str]
    summary: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    """Schema for resume upload response."""
    resume: ResumeResponse
    analysis: ResumeAnalysis
    message: str


# ==================== Job Schemas ====================

class JobBase(BaseModel):
    """Base schema for job."""
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    requirements: List[str] = []
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None


class JobCreate(JobBase):
    """Schema for creating a job."""
    pass


class JobResponse(JobBase):
    """Schema for job response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Job Match Schemas ====================

class JobMatchResponse(BaseModel):
    """Schema for job match response."""
    id: int
    job_title: str
    company: Optional[str]
    job_description: Optional[str]
    match_score: int
    explanation: str
    matching_skills: List[str]
    missing_skills: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobRecommendationRequest(BaseModel):
    """Schema for requesting job recommendations."""
    resume_id: int
    num_recommendations: int = 5


class JobRecommendationResponse(BaseModel):
    """Schema for job recommendations response."""
    resume_summary: str
    recommendations: List[JobMatchResponse]
    total_matches: int
