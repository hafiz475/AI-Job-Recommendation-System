import React, { useState, useEffect } from 'react';
import type { Resume, JobMatch } from '../types';
import { getJobRecommendations } from '../api';
import ResumeCard from './ResumeCard';
import JobCard from './JobCard';
import './ResultsDashboard.css';

interface ResultsDashboardProps {
    resume: Resume;
    onReset: () => void;
}

const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ resume, onReset }) => {
    const [recommendations, setRecommendations] = useState<JobMatch[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                console.log('🔍 Fetching job recommendations for resume:', resume.id);
                const response = await getJobRecommendations(resume.id, 5);
                console.log('✅ Job recommendations received:', response);
                setRecommendations(response.recommendations || []);
            } catch (err) {
                console.error('❌ Error fetching recommendations:', err);
                setError(err instanceof Error ? err.message : 'Failed to get recommendations');
            } finally {
                setIsLoading(false);
            }
        };

        fetchRecommendations();
    }, [resume.id]);

    return (
        <div className="dashboard">
            <div className="dashboard-header animate-fade-in">
                <div className="header-content">
                    <h1>Your Job Matches</h1>
                    <p>AI-powered recommendations based on your resume analysis</p>
                </div>
                <button className="btn btn-secondary" onClick={onReset}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: 18, height: 18 }}>
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" x2="12" y1="3" y2="15" />
                    </svg>
                    Upload New Resume
                </button>
            </div>

            <div className="dashboard-grid">
                <aside className="dashboard-sidebar">
                    <ResumeCard resume={resume} />
                </aside>

                <main className="dashboard-main">
                    <div className="section-header">
                        <h2>Recommended Jobs</h2>
                        <span className="job-count">{recommendations.length} matches found</span>
                    </div>

                    {isLoading ? (
                        <div className="loading-state">
                            <div className="spinner"></div>
                            <p>Finding the best matches for you...</p>
                        </div>
                    ) : error ? (
                        <div className="error-state">
                            <p>{error}</p>
                            <button className="btn btn-primary" onClick={() => window.location.reload()}>Try Again</button>
                        </div>
                    ) : recommendations.length === 0 ? (
                        <div className="empty-state">
                            <p>No job recommendations found. Try uploading a different resume.</p>
                        </div>
                    ) : (
                        <div className="jobs-list">
                            {recommendations.map((job, i) => (
                                <JobCard key={job.id} job={job} index={i} />
                            ))}
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
};

export default ResultsDashboard;
