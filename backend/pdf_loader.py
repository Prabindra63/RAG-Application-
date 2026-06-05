"""PDF text extraction. (Task 1)"""
from pathlib import Path
import fitz

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text from PDF page-by-page."""
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text", sort=True)
            if text.strip():
                pages.append({"page": page_num, "text": text})

    return pages

