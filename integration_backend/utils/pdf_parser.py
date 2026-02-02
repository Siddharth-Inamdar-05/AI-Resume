"""
PDF Parser Utility
Extracts text from PDF files using PyMuPDF (fitz)
"""

import io
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF file bytes
    
    Args:
        pdf_bytes: Raw PDF file bytes
        
    Returns:
        Extracted text as a single string
        
    Raises:
        Exception: If PDF cannot be read or parsed
    """
    try:
        # Open PDF from bytes
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        
        # Extract text from all pages
        text_content = []
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            text_content.append(text)
        
        # Close the document
        pdf_document.close()
        
        # Join all pages with newlines
        full_text = "\n".join(text_content)
        
        return full_text.strip()
    
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")
