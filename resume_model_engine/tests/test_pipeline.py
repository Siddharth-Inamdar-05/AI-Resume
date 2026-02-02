"""
Basic tests for the resume screening pipeline.
"""

import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.cleaner import clean_text
from src.skill_extractor import extract_skills, compute_skill_matches
from src.regex_extractor import extract_contact_info
from src.similarity import compute_tfidf_similarity
from src.scorer import compute_skill_match_score, compute_final_score
from src.pipeline import evaluate_candidates


def test_cleaner():
    """Test text cleaning functionality."""
    print("Testing cleaner...")
    
    text = "  Hello   World\n\nPython & C++  "
    cleaned = clean_text(text)
    assert cleaned == "hello world python c++"
    
    # Test contractions
    text = "don't won't can't"
    cleaned = clean_text(text)
    assert "don" in cleaned and "t" in cleaned
    
    print("✓ Cleaner tests passed")


def test_skill_extractor():
    """Test skill extraction."""
    print("Testing skill extractor...")
    
    text = "I have experience with Python, TensorFlow, and AWS cloud services."
    cleaned = clean_text(text)
    skills = extract_skills(cleaned)
    
    print(f"  Extracted skills: {skills}")
    
    assert "python" in skills
    assert "tensorflow" in skills or "tf" in skills
    assert "aws" in skills or "amazon web services" in skills
    
    # Test skill matching
    jd_skills = ["python", "tensorflow", "aws", "docker"]
    resume_skills = ["python", "tensorflow", "git"]
    
    matches = compute_skill_matches(jd_skills, resume_skills)
    assert "python" in matches["matched"]
    assert "tensorflow" in matches["matched"]
    assert "docker" in matches["missing"]
    
    print("✓ Skill extractor tests passed")


def test_regex_extractor():
    """Test regex-based extraction."""
    print("Testing regex extractor...")
    
    text = """
    Email: test@example.com
    Phone: +91-9876543210
    GitHub: https://github.com/testuser
    LinkedIn: https://www.linkedin.com/in/testuser
    """
    
    info = extract_contact_info(text)
    
    assert len(info["emails"]) > 0
    assert "test@example.com" in info["emails"]
    assert len(info["phones"]) > 0
    assert len(info["github"]) > 0
    assert len(info["linkedin"]) > 0
    
    print("✓ Regex extractor tests passed")


def test_similarity():
    """Test TF-IDF similarity."""
    print("Testing similarity...")
    
    jd = "python machine learning tensorflow deep learning"
    resume = "python deep learning neural networks experience"
    
    score = compute_tfidf_similarity(jd, resume)
    
    assert 0 <= score <= 100
    assert score > 0  # Should have some similarity
    
    print(f"✓ Similarity tests passed (score: {score})")


def test_scorer():
    """Test scoring functions."""
    print("Testing scorer...")
    
    # Test skill match score
    matched = ["python", "sql"]
    total = ["python", "sql", "aws"]
    
    score = compute_skill_match_score(matched, total)
    assert abs(score - 66.67) < 1  # ~66.67%
    
    # Test final score
    final = compute_final_score(80.0, 60.0)
    assert abs(final - 70.0) < 0.1  # (0.5*80 + 0.5*60)
    
    print("✓ Scorer tests passed")


def test_pipeline():
    """Test full pipeline."""
    print("Testing full pipeline...")
    
    jd = """
    We need a Python developer with machine learning experience.
    Required: Python, TensorFlow, SQL, AWS
    """
    
    candidates = {
        "test_candidate_1": """
        John Doe
        Email: john@example.com
        Phone: 9876543210
        
        Skills: Python, TensorFlow, SQL, Machine Learning
        Experience: 5 years at TechCorp
        """,
        
        "test_candidate_2": """
        Jane Smith
        Email: jane@example.com
        
        Skills: JavaScript, React, Node.js
        Experience: 3 years at WebCo
        """
    }
    
    results = evaluate_candidates(jd, candidates)
    
    # Check output format
    assert len(results) == 2
    assert all("candidate_id" in r for r in results)
    assert all("final_match_score" in r for r in results)
    assert all("matched_skills" in r for r in results)
    assert all("short_reason" in r for r in results)
    
    # Check ranking (candidate 1 should rank higher)
    assert results[0]["final_match_score"] >= results[1]["final_match_score"]
    
    print(f"✓ Pipeline tests passed")
    print(f"  Candidate 1 score: {results[0]['final_match_score']}")
    print(f"  Candidate 2 score: {results[1]['final_match_score']}")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("RUNNING TESTS FOR RESUME SCREENING ENGINE")
    print("=" * 60 + "\n")
    
    try:
        test_cleaner()
        test_skill_extractor()
        test_regex_extractor()
        test_similarity()
        test_scorer()
        test_pipeline()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
