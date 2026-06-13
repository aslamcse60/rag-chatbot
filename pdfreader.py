import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    pages = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    
    return pages