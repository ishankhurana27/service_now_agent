def chunk_article(article_body: str, chunk_size: int = 800, overlap: int = 100):
    """
    Content-agnostic article chunking.

    - Operates ONLY on article body (not entire PDF)
    - Does NOT care about SQL or TEXT
    - Creates overlapping chunks for retrieval stability
    """

    if not article_body:
        return []

    text = article_body.strip()
    chunks = []

    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # move forward with overlap
        start = end - overlap
        if start < 0:
            start = 0

    return chunks
