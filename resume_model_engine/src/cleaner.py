"""
Text cleaning utilities for resume and job description preprocessing.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean and normalize text while preserving meaningful content.
    
    Args:
        text: Raw input text (resume or job description)
        
    Returns:
        Cleaned and normalized text
        
    Examples:
        >>> clean_text("  Hello   World\\n\\n  ")
        'hello world'
        >>> clean_text("Python, Java & C++")
        'python java c++'
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace multiple newlines/tabs with single space
    text = re.sub(r'[\n\r\t]+', ' ', text)
    
    # Remove extra whitespace (multiple spaces to single space)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep: alphanumeric, spaces, +, #, ., apostrophes
    # This preserves: C++, C#, .NET, don't, won't, etc.
    text = re.sub(r"[^a-z0-9\s+#.']", ' ', text)
    
    # Clean up any resulting multiple spaces again
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text
