def create_chunks(pages, chunk_line_limit=15, overlap_lines=3) -> list[dict]:
    """Split page text line-by-line with overlap (keeps table rows intact)."""
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
