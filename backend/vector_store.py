import json
import os
import pickle

import faiss
import numpy as np

VECTOR_DB_DIR = "vector_db"
INDEX_PATH = os.path.join(VECTOR_DB_DIR, "index.faiss")
CHUNK_PATH = os.path.join(VECTOR_DB_DIR, "chunks.pkl")
METADATA_PATH = os.path.join(VECTOR_DB_DIR, "metadata.json")

_index_cache: dict = {"mtime": None, "index": None, "chunks": None}


def invalidate_index_cache() -> None:
    _index_cache.update(mtime=None, index=None, chunks=None)


def load_index():
    """Load FAISS index + chunks from disk, with in-memory cache."""
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNK_PATH):
        raise FileNotFoundError("Vector index not found. Upload and index a PDF first.")

    mtime = os.path.getmtime(INDEX_PATH)
    if _index_cache["mtime"] != mtime:
        _index_cache["index"] = faiss.read_index(INDEX_PATH)
        with open(CHUNK_PATH, "rb") as f:
            _index_cache["chunks"] = pickle.load(f)
        _index_cache["mtime"] = mtime

    return _index_cache["index"], _index_cache["chunks"]


def save_to_faiss(embeddings, chunks, filename="unknown", num_pages=0) -> None:
    """Persist embeddings, chunks, and metadata; refresh cache."""
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)

    vectors = np.asarray(embeddings, dtype=np.float32)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    with open(CHUNK_PATH, "wb") as f:
        pickle.dump(chunks, f)

    metadata = {
        "filename": filename,
        "num_pages": num_pages,
        "num_chunks": len(chunks),
    }
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    invalidate_index_cache()
    load_index()


def clear_vector_store() -> None:
    """Delete index files and clear cache."""
    for path in (INDEX_PATH, CHUNK_PATH, METADATA_PATH):
        if os.path.exists(path):
            os.remove(path)
    invalidate_index_cache()
