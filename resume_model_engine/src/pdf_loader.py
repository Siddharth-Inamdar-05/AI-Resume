"""PDF loading utilities for the resume engine.

Provides functions to extract text from PDFs and load resumes or JDs from
disk. Uses PyMuPDF (fitz) for robust PDF text extraction.
"""
from pathlib import Path
import re
from typing import Dict

try:
    import fitz  # PyMuPDF
except Exception as e:
    fitz = None  # type: ignore


def _normalize_text(text: str) -> str:
    """Basic cleaning of extracted text.

    - Collapse multiple whitespace characters into a single space.
    - Strip leading/trailing whitespace.
    """
    return re.sub(r"\s+", " ", text).strip()


def pdf_to_text(pdf_path: Path) -> str:
    """Extract text from all pages of a PDF using PyMuPDF.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a single string. Returns empty string on failure.
    """
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) is not installed")

    pdf_path = Path(pdf_path)
    if not pdf_path.exists() or not pdf_path.is_file():
        return ""

    try:
        doc = fitz.open(str(pdf_path))
        parts = []
        for page in doc:
            try:
                text = page.get_text() or ""
                parts.append(text)
            except Exception:
                # Skip a single page on failure
                continue
        doc.close()
        full_text = "\n".join(parts)
        return _normalize_text(full_text)
    except Exception:
        return ""


def load_resumes_from_folder(folder_path: str) -> Dict[str, str]:
    """Load all PDF resumes from a folder into a dict.

    Args:
        folder_path: Path to folder containing PDF files

    Returns:
        Dictionary mapping candidate_id (filename without extension) to
        extracted resume text. Files that fail extraction or yield empty
        text are skipped.
    """
    folder = Path(folder_path)
    results: Dict[str, str] = {}

    if not folder.exists() or not folder.is_dir():
        return results

    for p in sorted(folder.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() != ".pdf":
            continue

        candidate_id = p.stem
        try:
            text = pdf_to_text(p)
        except Exception as e:
            print(f"[pdf_loader] Failed to read '{p.name}': {e}")
            continue

        if not text:
            print(f"[pdf_loader] Skipping '{p.name}' — no text extracted")
            continue

        results[candidate_id] = text

    return results


def load_jd_from_file(jd_path: str) -> str:
    """Load job description text from a plain text file.

    Args:
        jd_path: Path to the .txt file containing the job description

    Returns:
        The job description text. Returns empty string if file missing.
    """
    p = Path(jd_path)
    if not p.exists() or not p.is_file():
        return ""

    try:
        content = p.read_text(encoding="utf-8")
        return _normalize_text(content)
    except Exception:
        return ""
