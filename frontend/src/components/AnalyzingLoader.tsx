import React, { useState, useEffect } from 'react';
import './AnalyzingLoader.css';

const steps = [
    { label: 'Reading your resume...', icon: '📄' },
    { label: 'Extracting skills...', icon: '🔍' },
    { label: 'Analyzing background...', icon: '🧠' },
    { label: 'Finding matches...', icon: '🎯' },
    { label: 'Preparing recommendations...', icon: '✨' },
];

const AnalyzingLoader: React.FC = () => {
    const [currentStep, setCurrentStep] = useState(0);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        const stepInt = setInterval(() => setCurrentStep((p) => (p + 1) % steps.length), 2500);
        const progInt = setInterval(() => setProgress((p) => (p >= 95 ? p : p + Math.random() * 3)), 300);
        return () => { clearInterval(stepInt); clearInterval(progInt); };
    }, []);

    return (
        <div className="analyzing-container">
            <div className="analyzing-content animate-fade-in">
                <div className="brain-animation">
                    <div className="brain-circle"><div className="brain-pulse"></div><div className="brain-icon">🧠</div></div>
                    <div className="orbit"><div className="orbit-dot"></div></div>
                    <div className="orbit orbit-2"><div className="orbit-dot"></div></div>
                </div>
                <h2>AI is Analyzing Your Resume</h2>
                <p className="analyzing-subtitle">Using AI to understand your unique skills and experience.</p>
                <div className="analyzing-steps">
                    {steps.map((step, i) => (
                        <div key={i} className={`analyzing-step ${i === currentStep ? 'active' : ''} ${i < currentStep ? 'completed' : ''}`}>
                            <span className="step-icon">{step.icon}</span>
                            <span className="step-label">{step.label}</span>
                            {i === currentStep && <div className="step-pulse"></div>}
                        </div>
                    ))}
                </div>
                <div className="analyzing-progress">
                    <div className="progress-bar"><div className="progress-bar-fill" style={{ width: `${progress}%` }}></div></div>
                    <span className="progress-text">{Math.round(progress)}%</span>
                </div>
                <p className="analyzing-tip">💡 Tip: Our AI considers skills, experience level, and career trajectory.</p>
            </div>
        </div>
    );
};

export default AnalyzingLoader;
