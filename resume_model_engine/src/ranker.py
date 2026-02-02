"""
Candidate ranking and reason generation.
"""

from typing import List, Dict


def generate_short_reason(
    skill_match_score: float,
    matched_skills: List[str],
    missing_skills: List[str],
    semantic_score: float
) -> str:
    """
    Generate rule-based short reason for match assessment.
    
    Args:
        skill_match_score: Skill match percentage (0-100)
        matched_skills: List of matched skills
        missing_skills: List of missing skills
        semantic_score: Semantic similarity score (0-100)
        
    Returns:
        2-3 line reason string
    """
    # Categorize match level
    if skill_match_score >= 80:
        match_level = "Strong match"
    elif skill_match_score >= 60:
        match_level = "Good match"
    elif skill_match_score >= 40:
        match_level = "Moderate match"
    else:
        match_level = "Weak match"
    
    # Build reason
    reason_parts = []
    
    # Primary assessment
    reason_parts.append(f"{match_level}: {skill_match_score:.0f}% skills matched.")
    
    # Semantic relevance
    if semantic_score >= 70:
        reason_parts.append("High semantic relevance.")
    elif semantic_score >= 50:
        reason_parts.append("Moderate semantic relevance.")
    else:
        reason_parts.append("Low semantic relevance.")
    
    # Missing skills (if any and if significant)
    if missing_skills and skill_match_score < 80:
        top_missing = missing_skills[:3]  # Show top 3 missing
        missing_str = ", ".join(top_missing)
        if len(missing_skills) > 3:
            missing_str += f" (+{len(missing_skills) - 3} more)"
        reason_parts.append(f"Missing: {missing_str}.")
    
    return " ".join(reason_parts)


def rank_candidates(candidates: List[Dict]) -> List[Dict]:
    """
    Rank candidates by final match score in descending order.
    
    Also generates 'short_reason' for each candidate.
    
    Args:
        candidates: List of candidate result dictionaries
        
    Returns:
        Sorted list of candidates (highest score first)
    """
    # Generate short reason for each candidate
    for candidate in candidates:
        candidate["short_reason"] = generate_short_reason(
            skill_match_score=candidate.get("skill_match_score", 0),
            matched_skills=candidate.get("matched_skills", []),
            missing_skills=candidate.get("missing_skills", []),
            semantic_score=candidate.get("semantic_similarity_score", 0)
        )
    
    # Sort by final_match_score descending
    sorted_candidates = sorted(
        candidates,
        key=lambda x: x.get("final_match_score", 0),
        reverse=True
    )
    
    return sorted_candidates
