import { useState } from 'react';
import type { Resume, ResumeAnalysis } from './types';
import Header from './components/Header';
import ResumeUpload from './components/ResumeUpload';
import AnalyzingLoader from './components/AnalyzingLoader';
import ResultsDashboard from './components/ResultsDashboard';
import './App.css';

type AppStep = 'upload' | 'analyzing' | 'results';

function App() {
  const [step, setStep] = useState<AppStep>('upload');
  const [resume, setResume] = useState<Resume | null>(null);
  const [userEmail, setUserEmail] = useState('');

  const handleAnalyzing = () => {
    setStep('analyzing');
  };

  const handleUploadSuccess = (uploadedResume: Resume, _analysis: ResumeAnalysis) => {
    setResume(uploadedResume);
    setStep('results');
  };

  const handleReset = () => {
    setStep('upload');
    setResume(null);
  };

  const handleError = () => {
    setStep('upload');
  };

  return (
    <div className="app">
      <Header
        userEmail={step === 'results' ? userEmail : undefined}
        onReset={step === 'results' ? handleReset : undefined}
      />

      <main className="app-main">
        {step === 'upload' && (
          <ResumeUpload
            onUploadSuccess={handleUploadSuccess}
            onAnalyzing={handleAnalyzing}
            onError={handleError}
            userEmail={userEmail}
            setUserEmail={setUserEmail}
          />
        )}

        {step === 'analyzing' && <AnalyzingLoader />}

        {step === 'results' && resume && (
          <ResultsDashboard resume={resume} onReset={handleReset} />
        )}
      </main>
    </div>
  );
}

export default App;
