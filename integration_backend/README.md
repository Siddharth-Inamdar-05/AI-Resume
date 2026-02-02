# Integration Backend for AI Resume Screening System

## Overview

This integration backend serves as a **bridge** between the Website frontend and the `resume_model_engine` without modifying any existing code. It provides a FastAPI-based REST API that:

1. Accepts job descriptions and resume PDFs from the frontend
2. Extracts text from PDFs using PyMuPDF
3. Calls the existing model engine (`resume_model_engine/src/pipeline.py`)
4. Returns structured evaluation results

## Architecture

```
Website Frontend (React/HTML)
         ↓
    HTTP POST /api/evaluate
         ↓
Integration Backend (FastAPI) ← this folder
         ↓
    resume_model_engine/src/pipeline.py (unchanged)
         ↓
    AI Model Evaluation
         ↓
    JSON Response to Frontend
```

## How It Connects to the Model

The integration backend imports the model **without editing it**:

```python
from resume_model_engine.src.pipeline import evaluate_candidates
```

The `sys.path` is adjusted in `main.py` to ensure the import works correctly:

```python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

This allows seamless integration while keeping all existing code untouched.

## API Endpoint

### `POST /api/evaluate`

**Content-Type:** `multipart/form-data`

**Request Fields:**
- `jd_text` (string, required): Job description text
- `resumes` (files, required): Multiple PDF resume files

**Example Request (JavaScript FormData):**

```javascript
const formData = new FormData();
formData.append('jd_text', jobDescriptionText);

// Add multiple resume files
resumeFiles.forEach(file => {
  formData.append('resumes', file);
});

fetch('http://localhost:8000/api/evaluate', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response JSON:**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_candidates": 5,
  "results": [
    {
      "name": "candidate1",
      "skill_match_score": 85.5,
      "semantic_similarity_score": 0.78,
      "final_match_score": 81.2,
      "matched_skills": ["Python", "Machine Learning", "FastAPI"],
      "jd_skills": ["Python", "Machine Learning", "FastAPI", "Docker"],
      "resume_skills": ["Python", "Machine Learning", "FastAPI", "React"],
      "contact_info": {
        "emails": ["candidate@example.com"],
        "phones": ["+1234567890"]
      }
    }
    // ... more candidates
  ],
  "processing_time_sec": 3.45,
  "skipped_files": [
    {
      "filename": "corrupted_resume.pdf",
      "reason": "Empty or unreadable PDF"
    }
  ]
}
```

## Installation & Setup

### 1. Install Dependencies

```bash
cd integration_backend
pip install -r requirements.txt
```

### 2. Download Spacy Model

The model engine requires spaCy's English language model:

```bash
python -m spacy download en_core_web_sm
```

### 3. Run the Server

**Option A: Using Uvicorn (recommended for development)**

```bash
uvicorn main:app --reload --port 8000
```

**Option B: Direct Python execution**

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 4. Verify Server is Running

Open your browser and navigate to:
- `http://localhost:8000` - Root endpoint
- `http://localhost:8000/docs` - Interactive API documentation
- `http://localhost:8000/health` - Health check with model status

## Connecting the Frontend

### If Frontend Has API Base URL Configuration

If the Website frontend has an environment variable or config file for API base URL (e.g., `REACT_APP_API_URL`, `API_BASE_URL`, etc.), update it to:

```
http://localhost:8000
```

Then the frontend should call:
```
${API_BASE_URL}/api/evaluate
```

### If Frontend Uses Hardcoded URLs

You'll need to manually update the frontend code to point to:
```
http://localhost:8000/api/evaluate
```

Alternatively, configure a reverse proxy or modify CORS settings as needed.

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful evaluation
- **400 Bad Request**: Missing `jd_text`, no resumes, or all files skipped
- **500 Internal Server Error**: Model evaluation failure

**Skipped Files:**
If a PDF cannot be processed (empty, corrupted, or not a PDF), it will be listed in the `skipped_files` array with a reason. The evaluation will continue with remaining valid files.

## Features

✅ **Stateless**: No data stored on disk  
✅ **In-memory processing**: All operations in RAM  
✅ **CORS enabled**: Works with localhost frontend  
✅ **Error resilient**: Skips bad PDFs and continues processing  
✅ **Fast**: Direct model invocation without overhead  
✅ **Zero changes**: No modifications to existing code  

## File Structure

```
integration_backend/
├── main.py                 # FastAPI server with /api/evaluate endpoint
├── utils/
│   └── pdf_parser.py      # PDF text extraction using PyMuPDF
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development

### Testing the API

Use the built-in Swagger UI at `http://localhost:8000/docs` to test the API interactively.

Or use cURL:

```bash
curl -X POST "http://localhost:8000/api/evaluate" \
  -F "jd_text=We are looking for a Python developer with ML experience" \
  -F "resumes=@resume1.pdf" \
  -F "resumes=@resume2.pdf"
```

### Hot Reload

When running with `--reload` flag, the server automatically restarts when code changes are detected.

## Production Deployment

For production:

1. **Update CORS origins** in `main.py` to specific domains instead of `["*"]`
2. **Use a production ASGI server** like Gunicorn with Uvicorn workers:
   ```bash
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```
3. **Add authentication** if needed
4. **Set up HTTPS** using a reverse proxy (nginx, Caddy)
5. **Add rate limiting** and request validation

## Troubleshooting

### Import Error: Cannot find `resume_model_engine`

Ensure you're running the server from the `integration_backend/` directory and that the `resume_model_engine/` folder exists in the project root (one level up).

### Spacy Model Not Found

Run:
```bash
python -m spacy download en_core_web_sm
```

### Port Already in Use

Change the port in the uvicorn command:
```bash
uvicorn main:app --reload --port 8001
```

## License

This integration layer follows the same license as the parent project.

1. cd integration_backend
2. uvicorn main:app --reload --port 8000
3. npm run dev