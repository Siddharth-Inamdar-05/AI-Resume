"""
Named Entity Recognition (NER) using spaCy.
"""

from typing import Dict, List
import spacy

# Global spaCy model (lazy loaded)
_nlp_model = None


def get_spacy_model():
    """
    Get or load spaCy model (singleton pattern).
    
    Returns:
        spaCy language model
    """
    global _nlp_model
    
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("en_core_web_sm")
        except OSError:
            print("Error: spaCy model 'en_core_web_sm' not found.")
            print("Please run: python -m spacy download en_core_web_sm")
            raise
    
    return _nlp_model


def extract_entities(text: str, max_entities_per_type: int = 10) -> Dict[str, List[str]]:
    """
    Extract named entities using spaCy NER.
    
    Extracts:
    - PERSON: People names
    - ORG: Organizations, companies
    - GPE: Geopolitical entities (cities, countries)
    - DATE: Dates and time periods
    
    Args:
        text: Input text (resume)
        max_entities_per_type: Maximum number of unique entities per category
        
    Returns:
        Dictionary with entity types as keys and lists of entities as values
        
    Example:
        >>> extract_entities("John Doe worked at Google in New York from 2020-2023")
        {
            'PERSON': ['John Doe'],
            'ORG': ['Google'],
            'GPE': ['New York'],
            'DATE': ['2020-2023']
        }
    """
    if not text:
        return {
            "PERSON": [],
            "ORG": [],
            "GPE": [],
            "DATE": []
        }
    
    nlp = get_spacy_model()
    doc = nlp(text)
    
    # Collect entities by type
    entities = {
        "PERSON": [],
        "ORG": [],
        "GPE": [],
        "DATE": []
    }
    
    for ent in doc.ents:
        if ent.label_ in entities:
            # Add unique entities only
            entity_text = ent.text.strip()
            if entity_text and entity_text not in entities[ent.label_]:
                entities[ent.label_].append(entity_text)
    
    # Limit to top N entities per type
    for ent_type in entities:
        entities[ent_type] = entities[ent_type][:max_entities_per_type]
    
    return entities
