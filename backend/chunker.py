"""Text chunking with overlap. (Task 2)"""
from backend.config import CHUNK_LINE_LIMIT, CHUNK_OVERLAP_LINES

def create_chunks(
    pages: list[dict],
    chunk_line_limit: int = CHUNK_LINE_LIMIT,
    overlap_lines: int = CHUNK_OVERLAP_LINES,
) -> list[dict]:
    """Split text into overlapping chunks to preserve context."""
    chunks = []
    step = max(chunk_line_limit - overlap_lines, 1)
    chunk_id = 0

    for page in pages:
        lines = page.get("text", "").split("\n")
        for i in range(0, len(lines), step):
            block = "\n".join(lines[i : i + chunk_line_limit]).strip()
            if block:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page["page"],
                    "content": block,
                })
                chunk_id += 1

    return chunks

