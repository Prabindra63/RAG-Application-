import os
import shutil
import tempfile

from backend.chunker import create_chunks
from backend.embeddings import generate_embeddings
from backend.pdf_loader import extract_text_from_pdf
from backend.rag_pipeline import generate_answer
from backend.retriever import get_metadata, retrieve_context
from backend.vector_store import clear_vector_store, save_to_faiss


def save_uploaded_pdf(file_bytes: bytes, filename: str) -> str:
    """Save uploaded PDF to temporary directory."""
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, filename)
    with open(pdf_path, "wb") as f:
        f.write(file_bytes)
    return pdf_path


def index_pdf(pdf_path: str, filename: str) -> dict:
    """Extract, chunk, embed, and save PDF to vector store."""
    pages = extract_text_from_pdf(pdf_path)
    chunks = create_chunks(pages)
    embeddings = generate_embeddings([c["content"] for c in chunks])
    save_to_faiss(embeddings, chunks, filename=filename, num_pages=len(pages))
    return {
        "num_pages": len(pages),
        "num_chunks": len(chunks),
    }


def document_status() -> dict | None:
    """Get current document metadata."""
    return get_metadata()


def ask_question(question: str, api_key: str) -> dict:
    """Retrieve context and generate answer."""
    chunks = retrieve_context(question)
    answer = generate_answer(question, chunks, api_key=api_key)
    return {
        "answer": answer,
        "sources": chunks,
    }


def reset_document() -> None:
    """Clear vector store and metadata."""
    clear_vector_store()
