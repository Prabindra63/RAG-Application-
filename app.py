import os
import streamlit as st

from backend.pdf_loader import extract_text_from_pdf
from backend.chunker import create_chunks

st.set_page_config(
    page_title="Financial Report RAG",
    layout="wide"
)

st.title("📊 Financial Report RAG")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    pdf_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )

    st.success("PDF uploaded successfully!")

    if st.button("Extract Text"):

        pages = extract_text_from_pdf(
            pdf_path
        )

        chunks = create_chunks(
            pages
        )

        st.success(
            f"""
Total Pages: {len(pages)}

Total Chunks: {len(chunks)}
"""
        )

        if len(chunks) > 0:

            st.subheader("First Chunk")

            st.write(
                chunks[0]["content"]
            )

            st.subheader(
                "Chunk Metadata"
            )

            st.json(
                {
                    "chunk_id": chunks[0]["chunk_id"],
                    "page": chunks[0]["page"]
                }
            )

        else:
            st.warning(
                "No text could be extracted from this PDF."
            )
            