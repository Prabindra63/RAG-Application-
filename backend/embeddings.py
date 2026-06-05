_model = None

EMBED_BATCH_SIZE = 64


def get_embedding_model():
    """Lazy-load SentenceTransformer (cached after first call)."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embeddings(texts: list[str]):
    """Return L2-normalized vectors for cosine similarity via inner product."""
    if not texts:
        return []
    model = get_embedding_model()
    return model.encode(
        texts,
        batch_size=EMBED_BATCH_SIZE,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=len(texts) > 200,
    )
