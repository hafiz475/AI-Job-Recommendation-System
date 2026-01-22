// API Types for the Job Recommendation System

export interface User {
  id: number;
  email: string;
  name?: string;
  created_at: string;
}

export interface ExperienceItem {
  title: string;
  company?: string;
  duration?: string;
  description?: string;
}

export interface EducationItem {
  degree: string;
  institution?: string;
  year?: string;
}

export interface ResumeAnalysis {
  skills: string[];
  experience: ExperienceItem[];
  education: EducationItem[];
  role_keywords: string[];
  summary: string;
}

export interface Resume {
  id: number;
  filename: string;
  skills: string[];
  experience: ExperienceItem[];
  education: EducationItem[];
  role_keywords: string[];
  summary?: string;
  created_at: string;
}

export interface ResumeUploadResponse {
  resume: Resume;
  analysis: ResumeAnalysis;
  message: string;
}

export interface JobMatch {
  id: number;
  job_title: string;
  company?: string;
  job_description?: string;
  match_score: number;
  explanation: string;
  matching_skills: string[];
  missing_skills: string[];
  created_at: string;
  location?: string;
  experience_level?: string;
  salary_range?: string;
  job_type?: string;
}

export interface JobRecommendationResponse {
  resume_summary: string;
  recommendations: JobMatch[];
  total_matches: number;
}

// UI State Types
export interface UploadState {
  isUploading: boolean;
  progress: number;
  error?: string;
}

export interface AppState {
  currentStep: 'upload' | 'analyzing' | 'results';
  resume?: Resume;
  recommendations?: JobMatch[];
  userEmail: string;
}
