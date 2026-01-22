import React from 'react';
import './Header.css';

interface HeaderProps {
    userEmail?: string;
    onReset?: () => void;
}

const Header: React.FC<HeaderProps> = ({ userEmail, onReset }) => {
    return (
        <header className="header">
            <div className="header-container">
                <div className="header-logo" onClick={onReset} style={{ cursor: onReset ? 'pointer' : 'default' }}>
                    <div className="logo-icon">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M20 7h-9" />
                            <path d="M14 17H5" />
                            <circle cx="17" cy="17" r="3" />
                            <circle cx="7" cy="7" r="3" />
                        </svg>
                    </div>
                    <div className="logo-text">
                        <span className="logo-title">JobMatch</span>
                        <span className="logo-subtitle">AI</span>
                    </div>
                </div>

                <nav className="header-nav">
                    <a href="#features" className="nav-link">Features</a>
                    <a href="#how-it-works" className="nav-link">How it Works</a>
                </nav>

                <div className="header-actions">
                    {userEmail && (
                        <div className="user-info">
                            <div className="user-avatar">
                                {userEmail.charAt(0).toUpperCase()}
                            </div>
                            <span className="user-email">{userEmail}</span>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
};

export default Header;
