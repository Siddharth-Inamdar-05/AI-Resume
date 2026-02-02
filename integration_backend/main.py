"""
Integration Backend for AI Resume Screening System
FastAPI server that connects the Website frontend to the resume_model_engine
"""

import sys
import time
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Adjust sys.path to import the model engine
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from resume_model_engine.src.pipeline import evaluate_candidates
except ImportError as e:
    raise ImportError(
        f"Failed to import evaluate_candidates from resume_model_engine: {e}\n"
        "Make sure the resume_model_engine folder exists in the project root."
    )

from utils.pdf_parser import extract_text_from_pdf

# Initialize FastAPI app
app = FastAPI(
    title="Resume Screening Integration API",
    description="Backend integration layer connecting frontend to AI model",
    version="1.0.0",
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # Common frontend dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_ner_keys(ner: Optional[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Ensure NER dict always contains PERSON/ORG/GPE/DATE keys."""
    if not isinstance(ner, dict):
        ner = {}

    return {
        "PERSON": ner.get("PERSON", []) or [],
        "ORG": ner.get("ORG", []) or [],
        "GPE": ner.get("GPE", []) or [],
        "DATE": ner.get("DATE", []) or [],
    }


def _sanitize_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes candidate output for frontend safety:
    - ensures all expected fields exist
    - ensures list fields return ['NA'] when empty
    - ensures ner_entities always has expected keys
    - ensures scores are floats
    """

    def na_list(val: Any) -> List[str]:
        if isinstance(val, list) and len(val) > 0:
            return val
        return ["NA"]

    def safe_float(val: Any) -> float:
        try:
            return float(val)
        except Exception:
            return 0.0

    ner_entities = _ensure_ner_keys(candidate.get("ner_entities"))

    return {
        "candidate_id": candidate.get("candidate_id", "NA"),

        "emails": na_list(candidate.get("emails", [])),
        "phones": na_list(candidate.get("phones", [])),
        "github": na_list(candidate.get("github", [])),
        "linkedin": na_list(candidate.get("linkedin", [])),

        "extracted_skills": candidate.get("extracted_skills", []) or [],
        "matched_skills": candidate.get("matched_skills", []) or [],
        "missing_skills": candidate.get("missing_skills", []) or [],

        "skill_match_score": safe_float(candidate.get("skill_match_score", 0.0)),
        "semantic_similarity_score": safe_float(candidate.get("semantic_similarity_score", 0.0)),
        "final_match_score": safe_float(candidate.get("final_match_score", 0.0)),

        "ner_entities": {
            "PERSON": ner_entities["PERSON"] if ner_entities["PERSON"] else ["NA"],
            "ORG": ner_entities["ORG"] if ner_entities["ORG"] else ["NA"],
            "GPE": ner_entities["GPE"] if ner_entities["GPE"] else ["NA"],
            "DATE": ner_entities["DATE"] if ner_entities["DATE"] else ["NA"],
        },

        "short_reason": candidate.get("short_reason", "NA"),
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Resume Screening Integration Backend",
        "status": "running",
        "version": "1.0.0",
    }


@app.post("/api/evaluate")
async def evaluate_resumes(
    jd_text: str = Form(...),
    resumes: List[UploadFile] = File(...),
) -> JSONResponse:
    """
    Evaluate resumes vs job description and return ranked candidates.
    """
    print("\n" + "="*60)
    print("📥 NEW EVALUATION REQUEST")
    print("="*60)
    print(f"JD Text Length: {len(jd_text)} characters")
    print(f"Number of Files: {len(resumes)}")
    print(f"File Names: {[f.filename for f in resumes]}")
    print("="*60 + "\n")
    
    start_time = time.time()
    job_id = str(uuid.uuid4())
    skipped_files: List[Dict[str, str]] = []

    # Validate inputs
    if not jd_text or jd_text.strip() == "":
        raise HTTPException(status_code=400, detail="Job description text is required")

    if not resumes or len(resumes) == 0:
        raise HTTPException(status_code=400, detail="At least one resume file is required")

    # Extract resume text from PDFs
    candidates: Dict[str, str] = {}

    for resume_file in resumes:
        filename = resume_file.filename or "unknown"

        # Only PDF files allowed
        if not filename.lower().endswith(".pdf"):
            skipped_files.append({"filename": filename, "reason": "Not a PDF file"})
            continue

        try:
            pdf_bytes = await resume_file.read()
            resume_text = extract_text_from_pdf(pdf_bytes)

            if not resume_text or resume_text.strip() == "":
                skipped_files.append({"filename": filename, "reason": "Empty or unreadable PDF"})
                continue

            candidate_id = Path(filename).stem
            candidates[candidate_id] = resume_text

        except Exception as e:
            skipped_files.append({"filename": filename, "reason": f"Error processing PDF: {str(e)}"})
            continue

    # Check if any candidate is valid
    if len(candidates) == 0:
        raise HTTPException(
            status_code=400,
            detail="No valid PDF resumes could be processed. All files were skipped.",
        )

    # Call model engine
    try:
        raw_results = evaluate_candidates(jd_text, candidates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during model evaluation: {str(e)}")

    # Sanitize output for frontend
    results = [_sanitize_candidate(c) for c in raw_results]

    processing_time = time.time() - start_time

    # Debug print
    print("\n--- MODEL OUTPUT DEBUG (first candidate) ---")
    if results:
        print(results[0])
    print("------------------------------------------\n")

    response_data = {
        "job_id": job_id,
        "total_candidates": len(candidates),
        "results": results,
        "processing_time_ms": int(processing_time * 1000),
        "processing_time_sec": round(processing_time, 2),
        "skipped_files": skipped_files,
    }

    return JSONResponse(content=response_data)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from resume_model_engine.src.pipeline import evaluate_candidates as _  # noqa: F401
        model_status = "available"
    except Exception as e:
        model_status = f"unavailable: {str(e)}"

    return {
        "status": "healthy",
        "model_engine": model_status,
        "timestamp": time.time(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
