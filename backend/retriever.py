import json
from pathlib import Path

import numpy as np

from backend.config import (
    METADATA_PATH,
    TOP_K_RETRIEVAL,
)

from backend.embeddings import (
    generate_embeddings,
)

from backend.vector_store import (
    load_index,
)

MIN_SIMILARITY = 0.25


def get_metadata():

    if not Path(
        METADATA_PATH
    ).exists():
        return None

    try:

        with open(
            METADATA_PATH,
            encoding="utf-8",
        ) as f:
            return json.load(f)

    except Exception:
        return None


def retrieve_context(
    query: str,
    top_k: int = TOP_K_RETRIEVAL,
):

    try:
        index, chunks = load_index()

    except FileNotFoundError:
        return []

    if not chunks:
        return []

    query_emb = np.asarray(
        generate_embeddings(
            [query]
        ),
        dtype=np.float32,
    )

    k = min(
        top_k,
        len(chunks),
    )

    scores, indices = index.search(
        query_emb,
        k,
    )

    results = []

    seen_pages = set()

    for score, idx in zip(
        scores[0],
        indices[0],
    ):

        if score < MIN_SIMILARITY:
            continue

        if (
            idx < 0
            or idx >= len(chunks)
        ):
            continue

        page = chunks[idx]["page"]

        if page in seen_pages:
            continue

        seen_pages.add(page)

        results.append(
            {
                **chunks[idx],
                "score": float(score),
            }
        )

    return results