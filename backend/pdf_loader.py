import fitz

def extract_text_from_pdf(pdf_path):
    """
    Extract text page-by-page from PDF
    and keep page metadata.
    """

    pages = []

    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):

        page = doc[page_num]

        text = page.get_text("text")

        pages.append({
            "page": page_num + 1,
            "text": text
        })

    doc.close()

    return pages