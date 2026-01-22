import React, { useState, useRef, useCallback } from 'react';
import type { Resume, ResumeAnalysis } from '../types';
import { uploadResume } from '../api';
import './ResumeUpload.css';

interface ResumeUploadProps {
    onUploadSuccess: (resume: Resume, analysis: ResumeAnalysis) => void;
    onAnalyzing: () => void;
    onError?: () => void;
    userEmail: string;
    setUserEmail: (email: string) => void;
}

const ResumeUpload: React.FC<ResumeUploadProps> = ({
    onUploadSuccess,
    onAnalyzing,
    onError,
    userEmail,
    setUserEmail,
}) => {
    const [isDragOver, setIsDragOver] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(false);
    }, []);

    const validateFile = (file: File): boolean => {
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
        const allowedExtensions = ['.pdf', '.docx', '.txt'];

        const extension = '.' + file.name.split('.').pop()?.toLowerCase();

        if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(extension)) {
            setError('Please upload a PDF, DOCX, or TXT file');
            return false;
        }

        if (file.size > 10 * 1024 * 1024) {
            setError('File size must be less than 10MB');
            return false;
        }

        return true;
    };

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(false);
        setError(null);

        const file = e.dataTransfer.files[0];
        if (file && validateFile(file)) {
            setSelectedFile(file);
        }
    }, []);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        setError(null);
        const file = e.target.files?.[0];
        if (file && validateFile(file)) {
            setSelectedFile(file);
        }
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleUpload = async () => {
        if (!selectedFile || !userEmail) {
            if (!userEmail) {
                setError('Please enter your email address');
            }
            return;
        }

        setIsUploading(true);
        setError(null);
        onAnalyzing();

        try {
            console.log('📤 Starting resume upload...');
            // Add timeout to prevent hanging
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('Request timeout. Please try again.')), 120000); // 2 minutes
            });

            const uploadPromise = uploadResume(selectedFile, userEmail);
            const response = await Promise.race([uploadPromise, timeoutPromise]) as any;
            
            console.log('✅ Resume upload successful:', response);
            setIsUploading(false);
            onUploadSuccess(response.resume, response.analysis);
        } catch (err) {
            console.error('❌ Resume upload error:', err);
            const errorMessage = err instanceof Error ? err.message : 'Failed to upload resume';
            setError(errorMessage);
            setIsUploading(false);
            // Reset to upload step on error
            if (onError) {
                onError();
            }
        }
    };

    const removeFile = () => {
        setSelectedFile(null);
        setError(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className="upload-section">
            <div className="upload-header animate-fade-in">
                <h1>Find Your Perfect Job Match</h1>
                <p className="upload-subtitle">
                    Upload your resume and let AI analyze your skills to find the best job opportunities tailored for you
                </p>
            </div>

            <div className="upload-content animate-fade-in stagger-1">
                {/* Email Input */}
                <div className="email-input-container">
                    <label htmlFor="email" className="input-label">Your Email</label>
                    <input
                        type="email"
                        id="email"
                        className="input email-input"
                        placeholder="you@example.com"
                        value={userEmail}
                        onChange={(e) => setUserEmail(e.target.value)}
                    />
                </div>

                {/* Upload Zone */}
                <div
                    className={`upload-zone ${isDragOver ? 'drag-over' : ''} ${selectedFile ? 'has-file' : ''}`}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={!selectedFile ? handleClick : undefined}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.docx,.txt"
                        onChange={handleFileSelect}
                        className="file-input"
                    />

                    {!selectedFile ? (
                        <>
                            <div className="upload-icon">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                    <polyline points="17 8 12 3 7 8" />
                                    <line x1="12" x2="12" y1="3" y2="15" />
                                </svg>
                            </div>
                            <h3>Drop your resume here</h3>
                            <p className="upload-hint">or click to browse</p>
                            <div className="upload-formats">
                                <span className="format-badge">PDF</span>
                                <span className="format-badge">DOCX</span>
                                <span className="format-badge">TXT</span>
                            </div>
                        </>
                    ) : (
                        <div className="selected-file">
                            <div className="file-icon">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                    <polyline points="14 2 14 8 20 8" />
                                    <line x1="16" x2="8" y1="13" y2="13" />
                                    <line x1="16" x2="8" y1="17" y2="17" />
                                    <polyline points="10 9 9 9 8 9" />
                                </svg>
                            </div>
                            <div className="file-info">
                                <span className="file-name">{selectedFile.name}</span>
                                <span className="file-size">
                                    {(selectedFile.size / 1024).toFixed(1)} KB
                                </span>
                            </div>
                            <button className="remove-file" onClick={removeFile}>
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <line x1="18" x2="6" y1="6" y2="18" />
                                    <line x1="6" x2="18" y1="6" y2="18" />
                                </svg>
                            </button>
                        </div>
                    )}
                </div>

                {/* Error Message */}
                {error && (
                    <div className="error-message animate-fade-in">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <circle cx="12" cy="12" r="10" />
                            <line x1="12" x2="12" y1="8" y2="12" />
                            <line x1="12" x2="12.01" y1="16" y2="16" />
                        </svg>
                        {error}
                    </div>
                )}

                {/* Upload Button */}
                <button
                    className="btn btn-primary btn-lg upload-button"
                    onClick={handleUpload}
                    disabled={!selectedFile || !userEmail || isUploading}
                >
                    {isUploading ? (
                        <>
                            <div className="spinner" style={{ width: 20, height: 20 }} />
                            Analyzing Resume...
                        </>
                    ) : (
                        <>
                            Analyze My Resume
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                style={{ width: 20, height: 20 }}
                            >
                                <path d="M5 12h14" />
                                <path d="m12 5 7 7-7 7" />
                            </svg>
                        </>
                    )}
                </button>
            </div>

            {/* Features Section */}
            <div className="features-grid animate-fade-in stagger-2">
                <div className="feature-card">
                    <div className="feature-icon skill-icon">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                        </svg>
                    </div>
                    <h3>Skill Extraction</h3>
                    <p>AI identifies your technical and soft skills from your resume</p>
                </div>

                <div className="feature-card">
                    <div className="feature-icon match-icon">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <circle cx="11" cy="11" r="8" />
                            <path d="m21 21-4.3-4.3" />
                        </svg>
                    </div>
                    <h3>Smart Matching</h3>
                    <p>Find jobs that perfectly align with your experience level</p>
                </div>

                <div className="feature-card">
                    <div className="feature-icon explain-icon">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                        </svg>
                    </div>
                    <h3>Detailed Explanations</h3>
                    <p>Understand exactly why each job matches your profile</p>
                </div>
            </div>
        </div>
    );
};

export default ResumeUpload;
