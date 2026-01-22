"""AI Service for resume analysis and job matching using Gemini or OpenAI."""
import json
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from app.config import settings


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume and extract structured data."""
        pass
    
    @abstractmethod
    async def generate_job_recommendations(
        self, 
        resume_analysis: Dict[str, Any],
        num_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate job recommendations based on resume analysis."""
        pass


class GeminiProvider(AIProvider):
    """Gemini AI provider implementation."""
    
    def __init__(self):
        import google.generativeai as genai
        
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key is not configured")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume using Gemini AI.
        
        Args:
            resume_text: Extracted text from resume
            
        Returns:
            Structured resume analysis data
        """
        prompt = f"""You are an expert HR professional and resume analyzer. Analyze the following resume and extract structured information.

RESUME TEXT:
{resume_text}

Please extract and return the following information in valid JSON format:
{{
    "skills": ["list of technical and soft skills found"],
    "experience": [
        {{
            "title": "Job Title",
            "company": "Company Name",
            "duration": "Duration (e.g., '2 years', 'Jan 2020 - Dec 2022')",
            "description": "Brief description of responsibilities"
        }}
    ],
    "education": [
        {{
            "degree": "Degree Name",
            "institution": "Institution Name",
            "year": "Graduation Year or Duration"
        }}
    ],
    "role_keywords": ["list of job titles/roles this person is suited for"],
    "summary": "A 2-3 sentence professional summary of the candidate"
}}

IMPORTANT:
- Extract ALL skills mentioned, including programming languages, frameworks, tools, and soft skills
- For experience, list in reverse chronological order
- For role_keywords, suggest 5-10 job titles this person would be qualified for
- Be thorough but concise
- Return ONLY valid JSON, no additional text

JSON Output:"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response (remove markdown code blocks if present)
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text.strip())
        except json.JSONDecodeError as e:
            # Return a default structure if parsing fails
            return {
                "skills": [],
                "experience": [],
                "education": [],
                "role_keywords": [],
                "summary": "Unable to parse resume. Please try again."
            }
        except Exception as e:
            raise ValueError(f"Gemini API error: {str(e)}")
    
    async def generate_job_recommendations(
        self, 
        resume_analysis: Dict[str, Any],
        num_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate job recommendations using Gemini AI.
        
        Args:
            resume_analysis: Structured resume analysis data
            num_recommendations: Number of job recommendations to generate
            
        Returns:
            List of job recommendations with explanations
        """
        skills = ", ".join(resume_analysis.get("skills", []))
        experience = json.dumps(resume_analysis.get("experience", []), indent=2)
        role_keywords = ", ".join(resume_analysis.get("role_keywords", []))
        summary = resume_analysis.get("summary", "")
        
        prompt = f"""You are an expert career advisor and job matching specialist. Based on the following candidate profile, generate {num_recommendations} highly relevant job recommendations.

CANDIDATE PROFILE:
Skills: {skills}
Experience: {experience}
Potential Roles: {role_keywords}
Summary: {summary}

Generate exactly {num_recommendations} job recommendations. For each job, provide:
1. A realistic job title
2. A company name (can be fictional but realistic)
3. A detailed job description (100-150 words)
4. A match score (0-100) based on how well the candidate fits
5. A detailed explanation of WHY this job matches the candidate (be specific about skills)
6. List of matching skills from the candidate's profile
7. List of skills the candidate might need to develop

Return the recommendations in this JSON format:
{{
    "recommendations": [
        {{
            "job_title": "Senior Software Engineer",
            "company": "TechCorp Inc.",
            "location": "Remote / San Francisco, CA",
            "job_description": "Detailed job description...",
            "match_score": 85,
            "explanation": "This job is an excellent match because you have X, Y, Z skills...",
            "matching_skills": ["Python", "React", "AWS"],
            "missing_skills": ["Kubernetes", "Go"],
            "experience_level": "Senior",
            "salary_range": "$120,000 - $160,000",
            "job_type": "Full-time"
        }}
    ]
}}

IMPORTANT:
- Make recommendations realistic and relevant to the candidate's experience level
- Explanations should be personalized and mention specific skills from their resume
- Match scores should be realistic (60-95 range typically)
- Vary the types of roles but keep them relevant
- Include a mix of match scores (not all high)
- Return ONLY valid JSON, no additional text

JSON Output:"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result.get("recommendations", [])
        except json.JSONDecodeError:
            return self._get_fallback_recommendations(resume_analysis, num_recommendations)
        except Exception as e:
            raise ValueError(f"Gemini API error: {str(e)}")
    
    def _get_fallback_recommendations(
        self, 
        resume_analysis: Dict[str, Any], 
        num_recommendations: int
    ) -> List[Dict[str, Any]]:
        """Generate fallback recommendations if AI fails."""
        skills = resume_analysis.get("skills", [])[:5]
        role_keywords = resume_analysis.get("role_keywords", ["Software Developer"])
        
        return [
            {
                "job_title": role_keywords[i % len(role_keywords)] if role_keywords else "Software Developer",
                "company": f"Tech Company {i + 1}",
                "location": "Remote",
                "job_description": f"We are looking for a talented professional to join our team. Key responsibilities include working with various technologies and collaborating with team members.",
                "match_score": 70 - (i * 5),
                "explanation": f"This role matches your skills in {', '.join(skills[:3]) if skills else 'your professional background'}.",
                "matching_skills": skills[:3],
                "missing_skills": [],
                "experience_level": "Mid-level",
                "salary_range": "Competitive",
                "job_type": "Full-time"
            }
            for i in range(num_recommendations)
        ]


class OpenAIProvider(AIProvider):
    """OpenAI provider implementation."""
    
    def __init__(self):
        from openai import OpenAI
        
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is not configured")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume using OpenAI."""
        prompt = f"""Analyze this resume and extract structured information in JSON format.

RESUME:
{resume_text}

Return JSON with: skills (array), experience (array of objects with title, company, duration, description), education (array), role_keywords (job titles suited for), summary (2-3 sentences).

Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume analyzer. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean up response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text.strip())
        except Exception as e:
            raise ValueError(f"OpenAI API error: {str(e)}")
    
    async def generate_job_recommendations(
        self, 
        resume_analysis: Dict[str, Any],
        num_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate job recommendations using OpenAI."""
        prompt = f"""Based on this candidate profile, generate {num_recommendations} job recommendations.

Profile: {json.dumps(resume_analysis)}

For each job include: job_title, company, location, job_description, match_score (0-100), explanation (personalized), matching_skills, missing_skills, experience_level, salary_range, job_type.

Return JSON with "recommendations" array. ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a career advisor. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result.get("recommendations", [])
        except Exception as e:
            raise ValueError(f"OpenAI API error: {str(e)}")


class AIService:
    """Main AI service that uses configured provider."""
    
    def __init__(self):
        self.provider: Optional[AIProvider] = None
    
    def _get_provider(self) -> AIProvider:
        """Get or initialize the AI provider."""
        if self.provider is None:
            if settings.ai_provider.lower() == "openai":
                self.provider = OpenAIProvider()
            else:
                self.provider = GeminiProvider()
        return self.provider
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume and extract structured data."""
        provider = self._get_provider()
        return await provider.analyze_resume(resume_text)
    
    async def generate_job_recommendations(
        self, 
        resume_analysis: Dict[str, Any],
        num_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate job recommendations based on resume analysis."""
        provider = self._get_provider()
        return await provider.generate_job_recommendations(
            resume_analysis, 
            num_recommendations
        )


# Create singleton instance
ai_service = AIService()
