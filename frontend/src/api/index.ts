// API service for communicating with the backend

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface ApiError {
    detail: string;
}

async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        let errorMessage = 'An error occurred';
        try {
            const error: ApiError = await response.json();
            errorMessage = error.detail || `Server error: ${response.status} ${response.statusText}`;
        } catch {
            errorMessage = `Server error: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }
    try {
        return await response.json();
    } catch (e) {
        throw new Error('Invalid response from server');
    }
}

// Resume API
export async function uploadResume(file: File, userEmail: string): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_email', userEmail);

    try {
        const response = await fetch(`${API_BASE_URL}/resume/upload`, {
            method: 'POST',
            body: formData,
        });

        return handleResponse(response);
    } catch (error) {
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Network error: Could not connect to server. Please check if the backend is running.');
        }
        throw error;
    }
}

export async function getResume(resumeId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/resume/${resumeId}`);
    return handleResponse(response);
}

export async function getUserResumes(userEmail: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/resume/user/${encodeURIComponent(userEmail)}`);
    return handleResponse(response);
}

// Job Recommendations API
export async function getJobRecommendations(
    resumeId: number,
    numRecommendations: number = 5
): Promise<any> {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_id: resumeId,
                num_recommendations: numRecommendations,
            }),
        });

        return handleResponse(response);
    } catch (error) {
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Network error: Could not connect to server. Please check if the backend is running.');
        }
        throw error;
    }
}

export async function getResumeRecommendations(resumeId: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/jobs/recommendations/resume/${resumeId}`);
    return handleResponse(response);
}

// User API
export async function createUser(email: string, name?: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, name }),
    });

    return handleResponse(response);
}

export async function getUserByEmail(email: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/users/email/${encodeURIComponent(email)}`);
    return handleResponse(response);
}

// Health check
export async function healthCheck(): Promise<any> {
    const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
    return handleResponse(response);
}
