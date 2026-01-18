from sentence_transformers import CrossEncoder

# Load once
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def build_rerank_text(query: str, doc: str, meta: dict) -> str:
    """
    Combine short description + content for better semantic judgment
    """
    short_desc = meta.get("short_description", "").strip()

    combined = f"""
Query:
{query}

Short Description:
{short_desc}

Content:
{doc}
""".strip()

    return combined

def rerank_chunks(query, docs, metas, top_k=10):
    """
    Cross-encoder reranking with short-description awareness
    """
    pairs = []

    for doc, meta in zip(docs, metas):
        short_desc = meta.get("short_description", "").strip()
        combined_text = f"{short_desc}\n\n{doc}".strip()
        pairs.append((query, combined_text))

    scores = cross_encoder.predict(pairs)

    scored = list(zip(docs, metas, scores))
    scored.sort(key=lambda x: x[2], reverse=True)

    return [(doc, meta) for doc, meta, _ in scored[:top_k]]
