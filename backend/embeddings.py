import hashlib
import logging

from backend.config import (
    EMBEDDING_MODEL,
    EMBED_BATCH_SIZE,
    EMBED_CACHE_SIZE,
)

logger = logging.getLogger(__name__)

_model = None
_embedding_cache = {}


def get_embedding_model():
    global _model

    if _model is None:
        from sentence_transformers import SentenceTransformer

        logger.info(
            f"Loading embedding model: {EMBEDDING_MODEL}"
        )

        _model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    return _model


def _hash_text(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def _get_cached_embedding(text: str):
    return _embedding_cache.get(
        _hash_text(text)
    )


def _cache_embedding(text: str, emb):

    if len(_embedding_cache) >= EMBED_CACHE_SIZE:

        oldest_key = next(
            iter(_embedding_cache)
        )

        del _embedding_cache[
            oldest_key
        ]

    _embedding_cache[
        _hash_text(text)
    ] = emb


def generate_embeddings(
    texts: list[str],
):
    """
    Returns:
        list[np.ndarray]
    """

    if not texts:
        return []

    model = get_embedding_model()

    results = [None] * len(texts)

    uncached_texts = []
    uncached_positions = []

    for pos, text in enumerate(texts):

        cached = _get_cached_embedding(
            text
        )

        if cached is not None:
            results[pos] = cached

        else:
            uncached_texts.append(text)
            uncached_positions.append(pos)

    if uncached_texts:

        embeddings = model.encode(
            uncached_texts,
            batch_size=EMBED_BATCH_SIZE,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        for text, pos, emb in zip(
            uncached_texts,
            uncached_positions,
            embeddings,
        ):
            results[pos] = emb
            _cache_embedding(
                text,
                emb,
            )

    return results