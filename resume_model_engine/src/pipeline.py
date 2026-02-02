
"""
Main pipeline orchestrating the entire resume screening process.
"""

#Final Score = (Skill Match Score * Skill Weight) + (Semantic Similarity Score * Semantic Weight)

from typing import Dict, List
from .cleaner import clean_text
from .skill_extractor import extract_skills, compute_skill_matches
from .regex_extractor import extract_contact_info
from .ner_extractor import extract_entities
from .similarity import compute_tfidf_similarity
from .scorer import compute_skill_match_score, compute_final_score
from .ranker import rank_candidates


def evaluate_candidates(
    jd_text: str,
    candidates: Dict[str, str],
    skill_weight: float = 0.50,
    semantic_weight: float = 0.50
) -> List[Dict]:
    """
    Main pipeline to evaluate and rank candidates against a job description.
    
    Args:
        jd_text: Job description text
        candidates: Dictionary mapping candidate_id to resume text
        skill_weight: Weight for skill matching (default 0.50)
        semantic_weight: Weight for semantic similarity (default 0.50)
        
    Returns:
        List of candidate result dictionaries, ranked by final_match_score
        
    Output format for each candidate:
        {
            "candidate_id": str,
            "emails": List[str],
            "phones": List[str],
            "github": List[str],
            "linkedin": List[str],
            "extracted_skills": List[str],
            "matched_skills": List[str],
            "missing_skills": List[str],
            "skill_match_score": float,
            "semantic_similarity_score": float,
            "final_match_score": float,
            "ner_entities": {
                "PERSON": List[str],
                "ORG": List[str],
                "GPE": List[str],
                "DATE": List[str]
            },
            "short_reason": str
        }
    
    Example:
        >>> jd = "We need a Python developer with ML experience"
        >>> resumes = {"candidate_1": "I have 5 years Python and ML experience..."}
        >>> results = evaluate_candidates(jd, resumes)
        >>> print(results[0]['final_match_score'])
        85.5
    """
    # Step 1: Clean job description
    jd_cleaned = clean_text(jd_text)
    
    # Step 2: Extract skills from JD
    jd_skills = extract_skills(jd_cleaned)
    
    # Step 3: Process each candidate
    results = []
    
    for candidate_id, resume_text in candidates.items():
        # Clean resume text
        resume_cleaned = clean_text(resume_text)
        
        # Extract resume skills
        resume_skills = extract_skills(resume_cleaned)
        
        # Compute skill matches
        skill_comparison = compute_skill_matches(jd_skills, resume_skills)
        matched_skills = skill_comparison["matched"]
        missing_skills = skill_comparison["missing"]
        
        # Extract contact information
        contact_info = extract_contact_info(resume_text)  # Use original text for better regex matching
        
        # Extract NER entities
        ner_entities = extract_entities(resume_text)  # Use original text for better NER
        
        # Compute semantic similarity
        semantic_score = compute_tfidf_similarity(jd_cleaned, resume_cleaned)
        
        # Compute skill match score
        skill_score = compute_skill_match_score(matched_skills, jd_skills)
        
        # Compute final weighted score
        final_score = compute_final_score(
            skill_score,
            semantic_score,
            skill_weight,
            semantic_weight
        )
        
        # Build result dictionary
        candidate_result = {
            "candidate_id": candidate_id,
            "emails": contact_info["emails"],
            "phones": contact_info["phones"],
            "github": contact_info["github"],
            "linkedin": contact_info["linkedin"],
            "extracted_skills": resume_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "skill_match_score": skill_score,
            "semantic_similarity_score": semantic_score,
            "final_match_score": final_score,
            "ner_entities": ner_entities,
            "short_reason": ""  # Will be filled by ranker
        }
        
        results.append(candidate_result)
    
    # Step 4: Rank candidates and generate reasons
    ranked_results = rank_candidates(results)
    
    return ranked_results
