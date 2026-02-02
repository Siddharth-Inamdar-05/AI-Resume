"""
Skill extraction module with synonym support.
"""

import re
from typing import List, Set
from pathlib import Path


# Skill synonyms and aliases mapping
SKILL_SYNONYMS = {
    "pytorch": ["pytorch", "torch"],
    "c++": ["c++", "cpp", "cplusplus"],
    "c#": ["c#", "csharp"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": ["natural language processing", "nlp"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "amazon web services": ["amazon web services", "aws"],
    "google cloud": ["google cloud", "gcp", "google cloud platform"],
    "microsoft azure": ["microsoft azure", "azure"],
    "node.js": ["node.js", "nodejs", "node"],
    "react.js": ["react.js", "react", "reactjs"],
    "vue.js": ["vue.js", "vue", "vuejs"],
    "angular.js": ["angular.js", "angular", "angularjs"],
    "tensorflow": ["tensorflow", "tf"],
    "kubernetes": ["kubernetes", "k8s"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "continuous integration": ["continuous integration", "ci/cd", "ci", "cd"],
    "object oriented programming": ["object oriented programming", "oop"],
    "test driven development": ["test driven development", "tdd"],
}


def load_skills(skills_file: str = None) -> Set[str]:
    """
    Load skills from CSV file.
    
    Args:
        skills_file: Path to skills.csv file. If None, uses default location.
        
    Returns:
        Set of unique skills (lowercase)
    """
    if skills_file is None:
        # Default path relative to this module
        current_dir = Path(__file__).parent.parent
        skills_file = current_dir / "data" / "skills.csv"
    
    skills = set()
    
    try:
        with open(skills_file, 'r', encoding='utf-8') as f:
            # Skip header
            next(f)
            for line in f:
                skill = line.strip().lower()
                if skill:
                    skills.add(skill)
    except FileNotFoundError:
        print(f"Warning: Skills file not found at {skills_file}. Using empty skill set.")
    
    return skills


def expand_skills_with_synonyms(skills: Set[str]) -> Set[str]:
    """
    Expand skill set with all known synonyms.
    
    Args:
        skills: Base set of skills
        
    Returns:
        Expanded set including synonyms
    """
    expanded = set(skills)
    
    for canonical, synonyms in SKILL_SYNONYMS.items():
        if canonical in skills:
            expanded.update(synonyms)
    
    return expanded


def extract_skills(text: str, skills_file: str = None) -> List[str]:
    """
    Extract skills from text using regex matching with word boundaries.
    
    Args:
        text: Input text (cleaned resume or job description)
        skills_file: Optional path to custom skills file
        
    Returns:
        List of unique extracted skills (sorted)
        
    Examples:
        >>> extract_skills("Experience with Python, TensorFlow and AWS cloud")
        ['aws', 'python', 'tensorflow']
    """
    if not text:
        return []
    
    text = text.lower()
    
    # Load base skills
    base_skills = load_skills(skills_file)
    
    # Expand with synonyms for matching
    all_skills = expand_skills_with_synonyms(base_skills)
    
    found_skills = set()
    
    # Match skills using word boundary regex
    for skill in all_skills:
        # Escape special regex characters in skill name
        escaped_skill = re.escape(skill)
        
        # Create pattern with word boundaries
        # Use \b for word boundaries, but handle special cases like C++, C#, .NET
        pattern = r'\b' + escaped_skill + r'\b'
        
        if re.search(pattern, text, re.IGNORECASE):
            # Map back to canonical skill if it's a synonym
            canonical_skill = skill
            for canonical, synonyms in SKILL_SYNONYMS.items():
                if skill in synonyms:
                    canonical_skill = canonical
                    break
            
            # Add the canonical or base skill
            if canonical_skill in base_skills:
                found_skills.add(canonical_skill)
            else:
                found_skills.add(skill)
    
    return sorted(list(found_skills))


def compute_skill_matches(jd_skills: List[str], resume_skills: List[str]) -> dict:
    """
    Compute matched and missing skills between JD and resume.
    
    Args:
        jd_skills: Skills extracted from job description
        resume_skills: Skills extracted from resume
        
    Returns:
        Dictionary with 'matched' and 'missing' skill lists
    """
    jd_set = set(jd_skills)
    resume_set = set(resume_skills)
    
    matched = sorted(list(jd_set.intersection(resume_set)))
    missing = sorted(list(jd_set - resume_set))
    
    return {
        "matched": matched,
        "missing": missing
    }
