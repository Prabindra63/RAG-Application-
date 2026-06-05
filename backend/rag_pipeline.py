import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_models: dict[str, genai.GenerativeModel] = {}


def _get_model(api_key: str) -> genai.GenerativeModel:
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    if model_name not in _models:
        genai.configure(api_key=api_key)
        _models[model_name] = genai.GenerativeModel(model_name)
    return _models[model_name]


def generate_answer(question: str, chunks: list[dict], api_key: str | None = None) -> str:
    """Generate a citation-backed answer using only retrieved context."""
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    context = "\n\n".join(
        f"--- Page {c['page']} ---\n{c['content']}" for c in chunks
    )

    prompt = f"""You are a Financial Report Assistant. Answer using ONLY the context below.

Rules:
- If the answer is not in the context, reply exactly: "Information not found in report."
- Cite page numbers like [Page 5] for every figure or claim.
- Do not use outside knowledge.

Context:
{context}

Question: {question}

Answer:"""

    response = _get_model(key).generate_content(prompt)
    return response.text or "Information not found in report."
