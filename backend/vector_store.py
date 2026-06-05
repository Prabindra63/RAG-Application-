import json
import pickle

import faiss
import numpy as np

from backend.config import (
    INDEX_PATH,
    CHUNK_PATH,
    METADATA_PATH,
)

_index_cache = {
    "mtime": None,
    "index": None,
    "chunks": None,
}


def invalidate_index_cache():
    _index_cache.update(
        mtime=None,
        index=None,
        chunks=None,
    )


def load_index():

    if (
        not INDEX_PATH.exists()
        or not CHUNK_PATH.exists()
    ):
        raise FileNotFoundError(
            "No indexed PDF found."
        )

    mtime = INDEX_PATH.stat().st_mtime

    if (
        _index_cache["mtime"]
        != mtime
    ):

        _index_cache[
            "index"
        ] = faiss.read_index(
            str(INDEX_PATH)
        )

        with open(
            CHUNK_PATH,
            "rb",
        ) as f:
            _index_cache[
                "chunks"
            ] = pickle.load(f)

        _index_cache[
            "mtime"
        ] = mtime

    return (
        _index_cache["index"],
        _index_cache["chunks"],
    )


def save_to_faiss(
    embeddings,
    chunks,
    filename="unknown",
    num_pages=0,
):

    vectors = np.asarray(
        embeddings,
        dtype=np.float32,
    )

    if len(vectors) == 0:
        raise ValueError(
            "No embeddings."
        )

    index = faiss.IndexFlatIP(
        vectors.shape[1]
    )

    index.add(vectors)

    faiss.write_index(
        index,
        str(INDEX_PATH),
    )

    with open(
        CHUNK_PATH,
        "wb",
    ) as f:
        pickle.dump(
            chunks,
            f,
        )

    metadata = {
        "filename": filename,
        "num_pages": num_pages,
        "num_chunks": len(chunks),
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            metadata,
            f,
            indent=2,
        )

    invalidate_index_cache()


def clear_vector_store():

    for path in (
        INDEX_PATH,
        CHUNK_PATH,
        METADATA_PATH,
    ):
        if path.exists():
            path.unlink()

    invalidate_index_cache()