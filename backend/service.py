import tempfile
import uuid
from pathlib import Path

from backend.pdf_loader import (
    extract_text_from_pdf,
)

from backend.chunker import (
    create_chunks,
)

from backend.embeddings import (
    generate_embeddings,
)

from backend.vector_store import (
    save_to_faiss,
    clear_vector_store,
)

from backend.retriever import (
    retrieve_context,
    get_metadata,
)

from backend.rag_pipeline import (
    generate_answer,
)


def save_uploaded_pdf(
    file_bytes: bytes,
    filename: str,
):

    path = (
        Path(
            tempfile.gettempdir()
        )
        /
        f"{uuid.uuid4()}_{filename}"
    )

    path.write_bytes(
        file_bytes
    )

    return str(path)


def index_pdf(
    pdf_path: str,
    filename: str,
):

    pages = extract_text_from_pdf(
        pdf_path
    )

    if not pages:
        raise ValueError(
            "No text found in PDF."
        )

    chunks = create_chunks(
        pages
    )

    if not chunks:
        raise ValueError(
            "No chunks created."
        )

    embeddings = (
        generate_embeddings(
            [
                c["content"]
                for c in chunks
            ]
        )
    )

    save_to_faiss(
        embeddings,
        chunks,
        filename=filename,
        num_pages=len(pages),
    )

    return {
        "num_pages": len(pages),
        "num_chunks": len(chunks),
    }


def document_status():
    return get_metadata()


def ask_question(
    question: str,
    api_key: str,
):

    chunks = retrieve_context(
        question
    )

    answer = generate_answer(
        question,
        chunks,
        api_key=api_key,
    )

    return {
        "answer": answer,
        "sources": chunks,
    }


def reset_document():
    clear_vector_store()