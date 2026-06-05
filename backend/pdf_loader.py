import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text page-by-page with geometric sorting (preserves table rows)."""
    pages = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text", sort=True)
            if text.strip():
                pages.append({"page": page_num, "text": text})
    return pages
