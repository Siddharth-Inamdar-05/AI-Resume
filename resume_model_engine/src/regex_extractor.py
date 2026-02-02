"""
Regex-based extraction of contact information and URLs.
"""

import re
from typing import List, Dict


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Input text
        
    Returns:
        List of unique email addresses
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return list(set(emails))


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract phone numbers (Indian and international formats).
    
    Supports:
    - +91-9876543210
    - +919876543210
    - 9876543210
    - (123) 456-7890
    - 123-456-7890
    
    Args:
        text: Input text
        
    Returns:
        List of unique phone numbers
    """
    phone_patterns = [
        r'\+91[-\s]?\d{10}',  # Indian with +91
        r'\+\d{1,3}[-\s]?\d{9,10}',  # International format
        r'\b\d{10}\b',  # 10-digit number
        r'\(\d{3}\)\s*\d{3}[-\s]?\d{4}',  # (123) 456-7890
        r'\b\d{3}[-\s]?\d{3}[-\s]?\d{4}\b',  # 123-456-7890
    ]
    
    phones = []
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        phones.extend(matches)
    
    # Deduplicate and clean
    unique_phones = list(set([p.strip() for p in phones]))
    return unique_phones


def extract_github_links(text: str) -> List[str]:
    """
    Extract GitHub profile/repository URLs.
    
    Args:
        text: Input text
        
    Returns:
        List of unique GitHub URLs
    """
    github_pattern = r'https?://(?:www\.)?github\.com/[\w\-]+'
    github_links = re.findall(github_pattern, text, re.IGNORECASE)
    return list(set(github_links))


def extract_linkedin_links(text: str) -> List[str]:
    """
    Extract LinkedIn profile URLs.
    
    Args:
        text: Input text
        
    Returns:
        List of unique LinkedIn URLs
    """
    linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[\w\-]+'
    linkedin_links = re.findall(linkedin_pattern, text, re.IGNORECASE)
    return list(set(linkedin_links))


def extract_contact_info(text: str) -> Dict[str, List[str]]:
    """
    Extract all contact information from text.
    
    Args:
        text: Input text (resume)
        
    Returns:
        Dictionary with emails, phones, github, and linkedin lists
        
    Example:
        >>> extract_contact_info("Email: john@example.com, Phone: +91-9876543210")
        {
            'emails': ['john@example.com'],
            'phones': ['+91-9876543210'],
            'github': [],
            'linkedin': []
        }
    """
    return {
        "emails": extract_emails(text),
        "phones": extract_phone_numbers(text),
        "github": extract_github_links(text),
        "linkedin": extract_linkedin_links(text)
    }
