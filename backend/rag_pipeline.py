import hashlib
import logging
from datetime import datetime, timedelta

import google.generativeai as genai

from backend.config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
)

logger = logging.getLogger(__name__)

_response_cache = {}
_cache_time = {}

CACHE_TTL = 3600
CACHE_SIZE = 100


def _get_model(api_key: str):

    genai.configure(
        api_key=api_key
    )

    return genai.GenerativeModel(
        GEMINI_MODEL
    )


def _cache_key(
    question: str,
    chunks: list[dict],
):

    content = "|".join(
        c["content"][:100]
        for c in chunks
    )

    return hashlib.sha256(
        f"{question}|{content}".encode()
    ).hexdigest()


def _is_valid(key):

    if key not in _cache_time:
        return False

    age = (
        datetime.now()
        - _cache_time[key]
    )

    return age < timedelta(
        seconds=CACHE_TTL
    )


def _cleanup():

    while len(_response_cache) > CACHE_SIZE:

        oldest = min(
            _cache_time,
            key=_cache_time.get,
        )

        _response_cache.pop(
            oldest,
            None,
        )

        _cache_time.pop(
            oldest,
            None,
        )


def generate_answer(
    question: str,
    chunks: list[dict],
    api_key: str | None = None,
):

    if not chunks:
        return (
            "Information not found in report."
        )

    key = api_key or GOOGLE_API_KEY

    cache_key = _cache_key(
        question,
        chunks,
    )

    if _is_valid(cache_key):
        return _response_cache[
            cache_key
        ]

    context = "\n\n".join(
        f"[Page {c['page']}]\n{c['content']}"
        for c in chunks
    )

    prompt = f"""
You are a Financial Report Assistant.

Rules:
- Use ONLY the provided context.
- Cite pages like [Page X].
- Never use outside knowledge.
- Never guess.
- If answer is unavailable say:
  Information not found in report.

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        model = _get_model(key)

        response = (
            model.generate_content(
                prompt
            )
        )

        answer = (
            response.text
            if response.text
            else (
                "Information not found in report."
            )
        )

        _response_cache[
            cache_key
        ] = answer

        _cache_time[
            cache_key
        ] = datetime.now()

        _cleanup()

        return answer

    except Exception as e:

        logger.exception(
            "Gemini error"
        )

        return (
            f"Error generating answer: {e}"
        )