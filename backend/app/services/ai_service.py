"""AI Service for resume analysis and job matching using Gemini or OpenAI."""
import json
import re
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


class DemoProvider(AIProvider):
    """Demo provider that works without API key - for testing."""
    
    # Common tech skills to look for
    TECH_SKILLS = [
        "python", "javascript", "java", "c++", "c#", "ruby", "go", "rust", "swift",
        "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi",
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "git", "linux", "ci/cd", "agile", "scrum",
        "machine learning", "deep learning", "tensorflow", "pytorch", "nlp",
        "html", "css", "typescript", "graphql", "rest api"
    ]
    
    SOFT_SKILLS = [
        "leadership", "communication", "teamwork", "problem solving", 
        "project management", "analytical", "creative", "detail-oriented"
    ]

    # Broader, multi-industry keywords so demo mode works for many resume types
    BUSINESS_SKILLS = [
        "excel", "power bi", "tableau", "sql", "data analysis", "data visualization",
        "business analysis", "requirements gathering", "stakeholder management",
        "kpi", "okr", "dashboard", "reporting", "forecasting", "budgeting",
        "financial modeling", "accounting", "bookkeeping", "quickbooks",
        "sap", "oracle", "netsuite", "erp", "crm", "salesforce", "hubspot",
        "market research", "competitive analysis", "pricing", "go-to-market",
        "seo", "sem", "google analytics", "ads", "campaign management", "content marketing",
        "customer success", "account management", "sales", "lead generation",
        "procurement", "supply chain", "logistics", "inventory management",
        "quality assurance", "iso", "compliance", "risk management",
        "customer service", "call center", "support", "ticketing", "zendesk", "freshdesk",
        "human resources", "recruitment", "talent acquisition", "payroll", "onboarding",
        "training", "learning and development", "performance management",
    ]

    HEALTHCARE_SKILLS = [
        "nursing", "registered nurse", "patient care", "clinical", "phlebotomy",
        "emr", "ehr", "epic", "cerner", "hipaa", "medical coding", "icd", "cpt",
        "radiology", "laboratory", "pharmacy", "therapist", "physiotherapy",
    ]

    EDUCATION_SKILLS = [
        "teaching", "curriculum", "lesson planning", "classroom management",
        "assessment", "learning outcomes", "student counseling", "mentoring",
        "training", "facilitation",
    ]

    DESIGN_SKILLS = [
        "ui", "ux", "figma", "sketch", "adobe xd", "photoshop", "illustrator",
        "branding", "graphic design", "wireframing", "prototyping", "user research",
    ]

    # Role patterns for many job families (kept simple for demo mode)
    ROLE_PATTERNS = [
        # Tech
        r"software engineer", r"developer", r"full[-\s]?stack", r"frontend", r"back[-\s]?end",
        r"data scientist", r"data engineer", r"devops", r"qa engineer", r"test engineer",
        r"product manager", r"project manager", r"scrum master",
        # Data / Business
        r"data analyst", r"business analyst", r"financial analyst", r"accountant", r"auditor",
        r"operations manager", r"operations analyst", r"supply chain", r"logistics",
        r"customer success", r"account manager", r"sales", r"sales executive",
        r"marketing", r"digital marketing", r"seo", r"content", r"brand manager",
        r"hr", r"human resources", r"recruiter", r"talent acquisition",
        # Healthcare / Education / Design
        r"nurse", r"registered nurse", r"medical", r"clinical", r"pharmacist",
        r"teacher", r"instructor", r"trainer",
        r"designer", r"graphic designer", r"ui/ux", r"ux designer", r"ui designer",
    ]
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Extract skills from resume using pattern matching."""
        text_lower = resume_text.lower()
        
        # Extract skills
        found_skills = []
        for skill in self.TECH_SKILLS:
            if skill in text_lower:
                found_skills.append(skill.title() if len(skill) > 3 else skill.upper())
        
        for skill in self.SOFT_SKILLS:
            if skill in text_lower:
                found_skills.append(skill.title())

        for skill in self.BUSINESS_SKILLS + self.HEALTHCARE_SKILLS + self.EDUCATION_SKILLS + self.DESIGN_SKILLS:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        # Extract potential job titles
        roles = []
        for pattern in self.ROLE_PATTERNS:
            if re.search(pattern, text_lower):
                # Turn pattern into a readable role label
                label = pattern.replace(r"[-\s]?", " ").replace("\\", "")
                label = re.sub(r"\s+", " ", label).strip()
                roles.append(label.title())
        
        if not roles:
            roles = ["Software Developer", "Technical Specialist"]
        
        # Generate summary
        summary = f"Professional with expertise in {', '.join(found_skills[:3]) if found_skills else 'technology'}. "
        summary += f"Suited for roles such as {', '.join(roles[:2])}."
        
        return {
            "skills": found_skills[:15] if found_skills else ["Programming", "Problem Solving"],
            "experience": [
                {"title": "Professional Experience", "company": "Various", "duration": "Multiple years", "description": "Technical work experience"}
            ],
            "education": [
                {"degree": "Relevant Degree", "institution": "University", "year": "Completed"}
            ],
            "role_keywords": roles[:5] + ["Technical Lead", "Senior Developer"],
            "summary": summary
        }
    
    async def generate_job_recommendations(
        self, 
        resume_analysis: Dict[str, Any],
        num_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate mock job recommendations that are tailored to the user's resume.
        
        Even in demo mode (without real AI APIs), we use the extracted
        role keywords and skills from the resume to build relevant titles
        and descriptions instead of fixed generic ones.
        """
        skills = resume_analysis.get("skills", []) or ["General Programming", "Problem Solving"]
        roles = resume_analysis.get("role_keywords", []) or ["Software Developer"]

        # Some sample companies to rotate through
        companies = [
            "TechVentures Inc.",
            "InnovateTech",
            "CloudSystems Co.",
            "Enterprise Solutions",
            "StartupHub",
            "ScaleUp Technologies",
            "DataFlow Analytics",
        ]

        # Base score we will decrease slightly for each additional recommendation
        base_score = 92

        recommendations: List[Dict[str, Any]] = []
        for i in range(num_recommendations):
            role_title = roles[i % len(roles)]
            company = companies[i % len(companies)]
            matching = skills[:5] if skills else ["Technical Skills"]

            score = max(60, base_score - i * 4)
            experience_level = "Senior" if score >= 85 else "Mid-level" if score >= 75 else "Junior / Entry-level"

            job_description = (
                f"We are looking for a {role_title} to join our team at {company}. "
                f"In this role, you will work with technologies such as {', '.join(matching[:3])}, "
                "collaborate with cross-functional teams, and help design and build scalable solutions. "
                "You should be comfortable taking ownership of features, writing clean code, and continuously learning."
            )

            explanation = (
                f"This position matches your background because of your experience with "
                f"{', '.join(matching[:3])}. "
                f"Your profile indicates that you are well suited for roles like {role_title}, "
                "so this opportunity aligns closely with your skills and trajectory."
            )

            recommendations.append(
                {
                    "job_title": role_title,
                    "company": company,
                    "location": "Remote / Hybrid",
                    "job_description": job_description,
                    "match_score": score,
                    "explanation": explanation,
                    "matching_skills": matching,
                    "missing_skills": [],
                    "experience_level": experience_level,
                    "salary_range": f"${90 + (score // 10) * 10},000 - ${110 + (score // 10) * 10},000",
                    "job_type": "Full-time",
                }
            )

        return recommendations


class GeminiProvider(AIProvider):
    """Gemini AI provider implementation."""
    
    def __init__(self):
        import google.generativeai as genai
        
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key is not configured")
        
        genai.configure(api_key=settings.gemini_api_key)
        # Try different model names for compatibility
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception:
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception:
                self.model = genai.GenerativeModel('gemini-1.0-pro')
    
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
            print(f"⚠️ JSON parse error, using demo analysis: {e}")
            demo = DemoProvider()
            return await demo.analyze_resume(resume_text)
        except Exception as e:
            # Fall back to demo mode on API error
            print(f"⚠️ Gemini API error, falling back to demo mode: {str(e)}")
            demo = DemoProvider()
            return await demo.analyze_resume(resume_text)
    
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
            print("⚠️ JSON parse error in job recommendations, using fallback")
            return self._get_fallback_recommendations(resume_analysis, num_recommendations)
        except Exception as e:
            print(f"⚠️ Gemini API error in job recommendations: {str(e)}")
            demo = DemoProvider()
            return await demo.generate_job_recommendations(resume_analysis, num_recommendations)
    
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
        self.provider_name: str = "demo"
    
    def _get_provider(self) -> AIProvider:
        """Get or initialize the AI provider. Falls back to Demo mode if no API key."""
        if self.provider is None:
            # Check if API keys are configured
            has_gemini = settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here"
            has_openai = settings.openai_api_key and settings.openai_api_key != "your_openai_api_key_here"
            
            if settings.ai_provider.lower() == "openai" and has_openai:
                print("🤖 Using OpenAI provider")
                self.provider = OpenAIProvider()
                self.provider_name = "openai"
            elif has_gemini:
                print("🤖 Using Gemini provider")
                self.provider = GeminiProvider()
                self.provider_name = "gemini"
            elif has_openai:
                print("🤖 Using OpenAI provider")
                self.provider = OpenAIProvider()
                self.provider_name = "openai"
            else:
                print("⚠️  No API key configured - Using Demo mode (add GEMINI_API_KEY or OPENAI_API_KEY to .env)")
                self.provider = DemoProvider()
                self.provider_name = "demo"
        return self.provider

    def get_provider_name(self) -> str:
        """Return the currently used provider name (demo/gemini/openai)."""
        # Ensure provider has been initialized at least once
        if self.provider is None:
            self._get_provider()
        return self.provider_name
    
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
