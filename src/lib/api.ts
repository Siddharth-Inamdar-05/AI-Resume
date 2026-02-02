import { EvaluationResponse, UploadedFile } from '@/types/candidate';

// API Configuration
// In development with Vite proxy: use empty string (calls /api/evaluate)
// In production: use full backend URL like "https://api.example.com"
const getBaseURL = (): string => {
    const envBaseURL = import.meta.env.VITE_API_BASE_URL;

    // If env var is not set or is empty, return empty (for proxy usage)
    if (!envBaseURL || envBaseURL.trim() === '') {
        return '';
    }

    // If env var is set, clean it up
    let base = envBaseURL.trim();

    // Remove trailing slash
    if (base.endsWith('/')) {
        base = base.slice(0, -1);
    }

    // If someone accidentally set it to "/api", remove it since we'll add it later
    if (base === '/api') {
        return '';
    }

    return base;
};

const API_BASE_URL = getBaseURL();

/**
 * Evaluate candidates using the backend AI model
 * @param jdText Job description text
 * @param files Uploaded resume files
 * @returns Evaluation response with candidate rankings
 */
export async function evaluateCandidates(
    jdText: string,
    files: UploadedFile[]
): Promise<EvaluationResponse> {
    // Construct URL - always append /api/evaluate to base
    const url = API_BASE_URL ? `${API_BASE_URL}/api/evaluate` : '/api/evaluate';

    console.log('🔗 API Configuration:');
    console.log('  Base URL from env:', import.meta.env.VITE_API_BASE_URL);
    console.log('  Normalized Base:', API_BASE_URL);
    console.log('  Final URL:', url);
    console.log('  JD Length:', jdText.length, 'characters');
    console.log('  Files:', files.length);
    console.log('  File names:', files.map(f => f.name));

    // Build FormData
    const formData = new FormData();
    formData.append('jd_text', jdText);

    // Add all resume files
    files.forEach((uploadedFile) => {
        formData.append('resumes', uploadedFile.file);
        console.log('  Adding file:', uploadedFile.name, `(${uploadedFile.size} bytes)`);
    });

    console.log('📤 Sending request to:', url);

    try {
        // Make API call
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            // Don't set Content-Type - browser will set it with boundary for multipart/form-data
        });

        console.log('📥 Response status:', response.status, response.statusText);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
            console.error('❌ API Error:', errorData);
            throw new Error(errorData.detail || `API Error: ${response.status}`);
        }

        const data = await response.json();

        console.log('✅ API Response received:');
        console.log('  Job ID:', data.job_id);
        console.log('  Total Candidates:', data.total_candidates);
        console.log('  Processing Time:', data.processing_time_ms, 'ms');
        console.log('  Results:', data.results?.length || 0, 'candidates');

        if (data.results && data.results.length > 0) {
            console.log('  First candidate:', data.results[0].candidate_id);
        }

        return data;
    } catch (error) {
        console.error('❌ Fetch Error:', error);
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Cannot connect to backend server. Make sure the backend is running at http://127.0.0.1:8000');
        }
        throw error;
    }
}
