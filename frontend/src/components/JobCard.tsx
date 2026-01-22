import React, { useState } from 'react';
import type { JobMatch } from '../types';
import './JobCard.css';

interface JobCardProps {
    job: JobMatch;
    index: number;
}

const JobCard: React.FC<JobCardProps> = ({ job, index }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const getScoreClass = (score: number) => {
        if (score >= 80) return 'high';
        if (score >= 60) return 'medium';
        return 'low';
    };

    return (
        <div className={`job-card card animate-fade-in stagger-${Math.min(index + 1, 5)}`}>
            <div className="job-card-header">
                <div className="job-info">
                    <h3 className="job-title">{job.job_title}</h3>
                    {job.company && <span className="job-company">{job.company}</span>}
                    <div className="job-meta">
                        {job.location && <span className="meta-item">📍 {job.location}</span>}
                        {job.job_type && <span className="meta-item">💼 {job.job_type}</span>}
                        {job.salary_range && <span className="meta-item">💰 {job.salary_range}</span>}
                    </div>
                </div>
                <div className={`match-score ${getScoreClass(job.match_score)}`}>
                    {job.match_score}%
                </div>
            </div>

            <div className="job-explanation">
                <div className="explanation-header">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 15h-2v-2h2zm0-4h-2V7h2z" />
                    </svg>
                    <span>Why This Matches</span>
                </div>
                <p>{job.explanation}</p>
            </div>

            <div className="job-skills">
                {job.matching_skills.length > 0 && (
                    <div className="skill-section">
                        <span className="skill-label">✓ Your Matching Skills:</span>
                        <div className="skill-list">
                            {job.matching_skills.map((skill, i) => (
                                <span key={i} className="skill-tag match">{skill}</span>
                            ))}
                        </div>
                    </div>
                )}
                {job.missing_skills.length > 0 && (
                    <div className="skill-section">
                        <span className="skill-label">↑ Skills to Develop:</span>
                        <div className="skill-list">
                            {job.missing_skills.map((skill, i) => (
                                <span key={i} className="skill-tag missing">{skill}</span>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            {job.job_description && (
                <>
                    <button className="expand-btn" onClick={() => setIsExpanded(!isExpanded)}>
                        {isExpanded ? 'Hide Description' : 'View Full Description'}
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                            style={{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}>
                            <polyline points="6 9 12 15 18 9" />
                        </svg>
                    </button>
                    {isExpanded && (
                        <div className="job-description animate-fade-in">
                            <p>{job.job_description}</p>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default JobCard;
