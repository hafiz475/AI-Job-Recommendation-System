"""Resume upload and analysis API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import User, Resume
from app.schemas import ResumeResponse, ResumeUploadResponse, ResumeAnalysis
from app.services.resume_parser import resume_parser
from app.services.ai_service import ai_service

router = APIRouter(prefix="/resume", tags=["Resume"])

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    user_email: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload and analyze a resume file.
    
    This endpoint:
    1. Validates the file format and size
    2. Extracts text from the resume
    3. Uses AI to analyze the resume and extract skills, experience, etc.
    4. Stores the results in the database
    
    Args:
        file: Resume file (PDF, DOCX, or TXT)
        user_email: Email of the user uploading the resume
        db: Database session
        
    Returns:
        Resume analysis results
    """
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Get or create user
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        user = User(email=user_email)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    try:
        # Parse resume
        raw_text = resume_parser.parse_resume(content, file.filename)
        cleaned_text = resume_parser.clean_text(raw_text)
        
        if not cleaned_text or len(cleaned_text) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract sufficient text from the resume. Please ensure the file is not corrupted."
            )
        
        # Analyze with AI
        analysis = await ai_service.analyze_resume(cleaned_text)
        
        # Deactivate previous resumes
        db.query(Resume).filter(
            Resume.user_id == user.id,
            Resume.is_active == True
        ).update({"is_active": False})
        
        # Create new resume record
        db_resume = Resume(
            user_id=user.id,
            filename=file.filename,
            raw_text=cleaned_text,
            skills=analysis.get("skills", []),
            experience=analysis.get("experience", []),
            education=analysis.get("education", []),
            role_keywords=analysis.get("role_keywords", []),
            summary=analysis.get("summary", "")
        )
        
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        
        # Build response
        resume_response = ResumeResponse(
            id=db_resume.id,
            filename=db_resume.filename,
            skills=db_resume.skills or [],
            experience=db_resume.experience or [],
            education=db_resume.education or [],
            role_keywords=db_resume.role_keywords or [],
            summary=db_resume.summary,
            created_at=db_resume.created_at
        )
        
        analysis_response = ResumeAnalysis(
            skills=analysis.get("skills", []),
            experience=[],  # Will be populated from the analysis
            education=[],
            role_keywords=analysis.get("role_keywords", []),
            summary=analysis.get("summary", "")
        )
        
        return ResumeUploadResponse(
            resume=resume_response,
            analysis=analysis_response,
            message="Resume uploaded and analyzed successfully!"
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
            detail=f"An error occurred while processing the resume: {str(e)}"
        )


@router.get("/user/{user_email}", response_model=List[ResumeResponse])
async def get_user_resumes(
    user_email: str,
    db: Session = Depends(get_db)
):
    """
    Get all resumes for a user.
    
    Args:
        user_email: User's email address
        db: Database session
        
    Returns:
        List of user's resumes
    """
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    resumes = db.query(Resume).filter(Resume.user_id == user.id).all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Get a specific resume by ID.
    
    Args:
        resume_id: Resume ID
        db: Database session
        
    Returns:
        Resume data
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Delete a resume by ID.
    
    Args:
        resume_id: Resume ID
        db: Database session
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    db.delete(resume)
    db.commit()
    return None
