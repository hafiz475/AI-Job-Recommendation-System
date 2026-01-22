"""Job recommendations API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Resume, JobMatch, User
from app.schemas import (
    JobMatchResponse, 
    JobRecommendationRequest, 
    JobRecommendationResponse
)
from app.services.ai_service import ai_service

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/recommend", response_model=JobRecommendationResponse)
async def get_job_recommendations(
    request: JobRecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered job recommendations based on a resume.
    
    This endpoint:
    1. Fetches the resume analysis
    2. Uses AI to generate relevant job recommendations
    3. Stores the recommendations in the database
    4. Returns recommendations with explanations
    
    Args:
        request: Job recommendation request containing resume_id
        db: Database session
        
    Returns:
        Job recommendations with match scores and explanations
    """
    # Get the resume
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    print(f"📋 Generating job recommendations for resume ID: {request.resume_id}")
    
    # Prepare resume analysis for AI
    resume_analysis = {
        "skills": resume.skills or [],
        "experience": resume.experience or [],
        "education": resume.education or [],
        "role_keywords": resume.role_keywords or [],
        "summary": resume.summary or ""
    }
    
    try:
        print("🤖 Starting AI job recommendation generation...")
        # Generate recommendations
        recommendations = await ai_service.generate_job_recommendations(
            resume_analysis,
            num_recommendations=request.num_recommendations
        )
        print(f"✅ Generated {len(recommendations)} job recommendations")
        
        # Store recommendations in database
        stored_recommendations = []
        for rec in recommendations:
            provider_name = ai_service.get_provider_name()
            explanation = rec.get("explanation", "") or ""
            if provider_name == "demo":
                explanation = (explanation + " (Note: demo mode uses keyword-based matching; for best accuracy configure GEMINI_API_KEY or OPENAI_API_KEY.)").strip()
            job_match = JobMatch(
                user_id=resume.user_id,
                resume_id=resume.id,
                job_title=rec.get("job_title", "Unknown Position"),
                company=rec.get("company"),
                job_description=rec.get("job_description"),
                match_score=rec.get("match_score", 0),
                explanation=explanation,
                matching_skills=rec.get("matching_skills", []),
                missing_skills=rec.get("missing_skills", [])
            )
            db.add(job_match)
            db.flush()  # Get the ID
            
            stored_recommendations.append(JobMatchResponse(
                id=job_match.id,
                job_title=job_match.job_title,
                company=job_match.company,
                job_description=job_match.job_description,
                match_score=job_match.match_score,
                explanation=job_match.explanation,
                matching_skills=job_match.matching_skills or [],
                missing_skills=job_match.missing_skills or [],
                created_at=job_match.created_at
            ))
        
        db.commit()
        
        return JobRecommendationResponse(
            resume_summary=resume.summary or "No summary available",
            recommendations=stored_recommendations,
            total_matches=len(stored_recommendations)
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.get("/recommendations/{user_email}", response_model=List[JobMatchResponse])
async def get_user_recommendations(
    user_email: str,
    db: Session = Depends(get_db)
):
    """
    Get all job recommendations for a user.
    
    Args:
        user_email: User's email address
        db: Database session
        
    Returns:
        List of job recommendations
    """
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    recommendations = db.query(JobMatch).filter(
        JobMatch.user_id == user.id
    ).order_by(JobMatch.match_score.desc()).all()
    
    return recommendations


@router.get("/recommendations/resume/{resume_id}", response_model=List[JobMatchResponse])
async def get_resume_recommendations(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all job recommendations for a specific resume.
    
    Args:
        resume_id: Resume ID
        db: Database session
        
    Returns:
        List of job recommendations
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    recommendations = db.query(JobMatch).filter(
        JobMatch.resume_id == resume_id
    ).order_by(JobMatch.match_score.desc()).all()
    
    return recommendations


@router.delete("/recommendation/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recommendation(match_id: int, db: Session = Depends(get_db)):
    """
    Delete a job recommendation.
    
    Args:
        match_id: Job match ID
        db: Database session
    """
    match = db.query(JobMatch).filter(JobMatch.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job recommendation not found"
        )
    
    db.delete(match)
    db.commit()
    return None
