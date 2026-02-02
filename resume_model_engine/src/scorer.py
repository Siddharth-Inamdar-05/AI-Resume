"""
Scoring logic for skill matching and final candidate scores.
"""

from typing import List


def compute_skill_match_score(matched_skills: List[str], total_jd_skills: List[str]) -> float:
    """
    Compute skill match percentage.
    
    Args:
        matched_skills: List of skills that matched between JD and resume
        total_jd_skills: List of all skills required in JD
        
    Returns:
        Skill match score on 0-100 scale
        
    Example:
        >>> compute_skill_match_score(['python', 'sql'], ['python', 'sql', 'aws'])
        66.67
    """
    if not total_jd_skills:
        return 0.0
    
    match_count = len(matched_skills)
    total_count = len(total_jd_skills)
    
    score = (match_count / total_count) * 100
    return round(score, 2)


def compute_final_score(
    skill_score: float, 
    semantic_score: float,
    skill_weight: float = 0.50,
    semantic_weight: float = 0.50
) -> float:
    """
    Compute weighted final match score.
    
    Args:
        skill_score: Skill match score (0-100)
        semantic_score: Semantic similarity score (0-100)
        skill_weight: Weight for skill score (default 0.50)
        semantic_weight: Weight for semantic score (default 0.50)
        
    Returns:
        Final weighted score on 0-100 scale
        
    Example:
        >>> compute_final_score(80.0, 60.0)
        70.0
    """
    # Ensure weights sum to 1.0
    total_weight = skill_weight + semantic_weight
    if total_weight == 0:
        return 0.0
    
    # Normalize weights
    skill_weight = skill_weight / total_weight
    semantic_weight = semantic_weight / total_weight
    
    # Compute weighted score
    final_score = (skill_weight * skill_score) + (semantic_weight * semantic_score)
    
    # Ensure score is in valid range
    final_score = max(0.0, min(100.0, final_score))
    
    return round(final_score, 2)
