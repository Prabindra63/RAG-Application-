import json
import os

from backend.embeddings import generate_embeddings
from backend.vector_store import METADATA_PATH, load_index


def get_metadata() -> dict | None:
    if not os.path.exists(METADATA_PATH):
        return None
    try:
        with open(METADATA_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def retrieve_context(query: str, top_k: int = 5) -> list[dict]:
    """Return top-k chunks most similar to the query."""
    index, chunks = load_index()
    query_emb = generate_embeddings([query])

    k = min(top_k, len(chunks))
    scores, indices = index.search(query_emb, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if 0 <= idx < len(chunks):
            results.append({**chunks[idx], "score": float(score)})
    return results
