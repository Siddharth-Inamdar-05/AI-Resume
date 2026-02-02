# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## AI Resume Screening Integration

This project connects to a Python-based AI model for resume screening and skill matching.

### Backend Setup

The backend API is located in the `integration_backend/` folder. To run it:

```bash
# Navigate to backend directory
cd integration_backend

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### API Endpoint

**POST** `/api/evaluate`

**Request Format:** `multipart/form-data`
- `jd_text` (string): Job description text
- `resumes` (files): Multiple PDF resume files

**Response Schema:**
```json
{
  "job_id": "uuid-string",
  "total_candidates": 5,
  "processing_time_ms": 3450,
  "results": [
    {
      "candidate_id": "resume_filename",
      "emails": ["email@example.com"],
      "phones": ["+1234567890"],
      "github": ["github.com/user"],
      "linkedin": ["linkedin.com/in/user"],
      "extracted_skills": ["Python", "React", "..."],
      "matched_skills": ["Python", "React"],
      "missing_skills": ["Docker"],
      "skill_match_score": 85.5,
      "semantic_similarity_score": 78.3,
      "final_match_score": 81.2,
      "ner_entities": {
        "PERSON": ["John Doe"],
        "ORG": ["Google", "Microsoft"],
        "GPE": ["San Francisco"],
        "DATE": ["2020", "2022"]
      },
      "short_reason": "Strong candidate with 8/10 required skills..."
    }
  ],
  "skipped_files": []
}
```

### NA Logic for Missing Fields

The UI automatically displays "NA" for any empty contact or entity fields:
- Empty `emails` array → Shows "NA"
- Empty `phones` array → Shows "NA"
- Empty `github` array → Shows "NA"
- Empty `linkedin` array → Shows "NA"
- Empty NER entity arrays (PERSON, ORG, GPE, DATE) → Shows "NA"

This ensures the UI never displays blank spaces or dummy data.

### Running the Full Application

1. **Start Backend** (Terminal 1):
   ```bash
   cd integration_backend
   uvicorn main:app --reload --port 8000
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   npm install
   npm run dev
   ```

3. Open browser to frontend URL (usually `http://localhost:8080`)
4. Upload PDF resumes and enter job description
5. Click "Evaluate Candidates" to see real AI-powered results

### Troubleshooting "Failed to Fetch" Error

If you see a "Failed to fetch" error, check these common issues:

#### 1. Backend Not Running
**Problem:** Backend server is not started  
**Solution:**
```bash
cd integration_backend
uvicorn main:app --reload --port 8000
```
**Verify:** Open http://127.0.0.1:8000 in browser - should see service info  
**Verify API docs:** Open http://127.0.0.1:8000/docs - should see Swagger UI

#### 2. Wrong Port
**Problem:** Backend is running on a different port  
**Solution:** Ensure backend runs on port 8000 (check the uvicorn command)  
**Check:** Look at the uvicorn startup message - it shows the port

#### 3. CORS Configuration
**Problem:** Browser blocks the request due to CORS policy  
**Solution:** The backend is configured to allow these origins:
- `http://localhost:5173`
- `http://localhost:8080`
- `http://127.0.0.1:5173`
- `http://127.0.0.1:8080`

If your frontend runs on a different port, update `integration_backend/main.py`:
```python
allow_origins=[
    "http://localhost:YOUR_PORT",
    "http://127.0.0.1:YOUR_PORT",
],
```

#### 4. Vite Proxy Not Working
**Problem:** Proxy configuration not active  
**Solution:** Restart the frontend dev server:
```bash
npm run dev
```

The Vite config includes a proxy that forwards `/api/*` requests to `http://127.0.0.1:8000`

#### 5. Check Browser Console
Open browser DevTools (F12) and check:
- **Console tab:** Look for detailed logs from the API call
- **Network tab:** Check if the request is being made and what the response is

#### 6. Verify API Call
The frontend should log these in the console:
```
🔗 API Configuration:
  Base URL: /api
  Full URL: /api/evaluate
  JD Length: XXX characters
  Files: X
```

If you don't see these logs, the evaluate function is not being called.

#### 7. ECONNREFUSED Error
**Problem:** `connect ECONNREFUSED 127.0.0.1:8000`  
**Solution:** Backend is not running or not accessible  

Steps to fix:
1. **Start the backend:**
   ```bash
   cd integration_backend
   uvicorn main:app --reload --port 8000
   ```
   
2. **Verify it's running:**
   - Open http://127.0.0.1:8000 in your browser
   - You should see: `{"service": "Resume Screening Integration Backend", ...}`
   
3. **Check the port:**
   - Make sure the uvicorn output says: `Uvicorn running on http://127.0.0.1:8000`
   - If it's on a different port, update `vite.config.ts` proxy target

#### 8. Double /api Prefix Error
**Problem:** Vite logs `[vite] http proxy error: /api/api/evaluate`  
**Solution:** API URL is being constructed incorrectly

The `.env` file should have:
```bash
VITE_API_BASE_URL=
```
(Leave it empty or unset)

**NOT:**
```bash
VITE_API_BASE_URL=/api  # ❌ This causes /api/api/evaluate
```

The frontend code will handle appending `/api/evaluate` automatically.

### How the Integration Works

```
User Action (Frontend)
  ↓
Index.tsx calls evaluateCandidates()
  ↓
src/lib/api.ts builds FormData
  ↓
Fetch POST to /api/evaluate
  ↓
Vite Proxy forwards to http://127.0.0.1:8000/api/evaluate
  ↓
FastAPI Backend (integration_backend/main.py)
  ↓
Extract text from PDFs using PyMuPDF
  ↓
Call resume_model_engine/src/pipeline.py
  ↓
evaluate_candidates() runs AI model
  ↓
Return results to backend
  ↓
Backend sanitizes and returns JSON
  ↓
Frontend receives and displays results
```

### Environment Variables

Create a `.env` file in the project root:

**For Development (using Vite proxy):**
```bash
# Leave empty to use Vite proxy
VITE_API_BASE_URL=
```

**For Production:**
```bash
# Use full backend URL
VITE_API_BASE_URL=https://your-backend-api.com
```

**Important:** 
- In development with Vite proxy, the base URL should be **empty**
- The frontend will call `/api/evaluate` directly
- Vite proxy will forward it to `http://127.0.0.1:8000/api/evaluate`
- Do NOT set `VITE_API_BASE_URL=/api` as this causes double `/api/api/evaluate`

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
#   A I - R e s u m e  
 