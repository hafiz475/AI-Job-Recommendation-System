import React from 'react';
import type { Resume } from '../types';
import './ResumeCard.css';

interface ResumeCardProps {
    resume: Resume;
}

const ResumeCard: React.FC<ResumeCardProps> = ({ resume }) => {
    return (
        <div className="resume-card card animate-fade-in">
            <div className="resume-card-header">
                <div className="resume-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                        <polyline points="14 2 14 8 20 8" />
                    </svg>
                </div>
                <div className="resume-meta">
                    <h3>{resume.filename}</h3>
                    <span className="resume-date">Uploaded {new Date(resume.created_at).toLocaleDateString()}</span>
                </div>
            </div>

            {resume.summary && (
                <div className="resume-summary">
                    <h4>Professional Summary</h4>
                    <p>{resume.summary}</p>
                </div>
            )}

            <div className="resume-section">
                <h4>Skills ({resume.skills.length})</h4>
                <div className="skills-container">
                    {resume.skills.slice(0, 12).map((skill, i) => (
                        <span key={i} className="skill-tag">{skill}</span>
                    ))}
                    {resume.skills.length > 12 && (
                        <span className="skill-tag more">+{resume.skills.length - 12} more</span>
                    )}
                </div>
            </div>

            <div className="resume-section">
                <h4>Potential Roles</h4>
                <div className="roles-container">
                    {resume.role_keywords.slice(0, 5).map((role, i) => (
                        <span key={i} className="role-badge">{role}</span>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ResumeCard;
