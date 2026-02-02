"""
Text similarity computation using TF-IDF and cosine similarity.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def compute_tfidf_similarity(jd_text: str, resume_text: str) -> float:
    """
    Compute TF-IDF based cosine similarity between job description and resume.
    
    Args:
        jd_text: Job description text (cleaned)
        resume_text: Resume text (cleaned)
        
    Returns:
        Similarity score on 0-100 scale
        
    Example:
        >>> compute_tfidf_similarity("python machine learning", "python deep learning")
        66.67
    """
    if not jd_text or not resume_text:
        return 0.0
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2)  # Unigrams and bigrams
    )
    
    try:
        # Fit and transform both texts
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        
        # Compute cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to 0-100 scale
        score = float(similarity * 100)
        
        # Ensure score is in valid range
        score = max(0.0, min(100.0, score))
        
        return round(score, 2)
    
    except Exception as e:
        print(f"Warning: Error computing TF-IDF similarity: {e}")
        return 0.0


# Future extension interface for SBERT/sentence-transformers
def compute_sbert_similarity(jd_text: str, resume_text: str) -> float:
    """
    Placeholder for SBERT-based semantic similarity.
    
    To implement:
    1. Install: pip install sentence-transformers
    2. Load model: model = SentenceTransformer('all-MiniLM-L6-v2')
    3. Encode texts: embeddings = model.encode([jd_text, resume_text])
    4. Compute cosine: similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    5. Return: similarity * 100
    
    Args:
        jd_text: Job description text
        resume_text: Resume text
        
    Returns:
        Similarity score on 0-100 scale
    """
    raise NotImplementedError(
        "SBERT similarity not yet implemented. "
        "Install sentence-transformers and implement this method."
    )
