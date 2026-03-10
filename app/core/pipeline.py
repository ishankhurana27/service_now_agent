from uuid import uuid4
from typing import Dict
from opentelemetry import trace

from app.ingestion.article_body_extractor import extract_article_body
from app.processing.article_chunker import chunk_article
from app.embeddings.embedder import embed_text
from app.vector_store.chroma_store import add_chunk

tracer = trace.get_tracer(__name__)


# --------------------------------------------------
# Fix 2: Instructional sentence detection
# --------------------------------------------------
ACTION_VERBS = (
    "log in",
    "login",
    "click",
    "select",
    "navigate",
    "go to",
    "access",
    "choose",
    "enter",
    "open",
    "review",
    "update",
    "submit"
)


def is_instructional_sentence(sentence: str) -> bool:
    s = sentence.strip().lower()
    return any(s.startswith(verb) for verb in ACTION_VERBS)


def run_pipeline(parsed_pdf: Dict):
    """
    FINAL ingestion pipeline

    - Extract ONLY article body
    - Prepend short description
    - Chunk irrespective of content
    - Embed and store with metadata
    """

    with tracer.start_as_current_span("pipeline_execution") as span:

        article_id = parsed_pdf["article_id"]
        span.set_attribute("article.id", article_id)

        # --------------------------------------------------
        # 1️⃣ Extract components
        # --------------------------------------------------
        short_desc = parsed_pdf.get("short_description", "").strip()
        article_body = extract_article_body(parsed_pdf)

        if not article_body and not short_desc:
            span.set_attribute("article.empty", True)
            return

        # --------------------------------------------------
        # 2️⃣ Build FULL semantic content
        # --------------------------------------------------
        if short_desc:
            full_text = f"Short Description:\n{short_desc}\n\n{article_body}"
        else:
            full_text = article_body

        span.set_attribute("article.text.length", len(full_text))

        # --------------------------------------------------
        # 2.1️⃣ Detect instructional sentences (Fix 2)
        # --------------------------------------------------
        instructional_sentences = []

        for line in full_text.splitlines():
            if is_instructional_sentence(line):
                instructional_sentences.append(line.strip())

        span.set_attribute(
            "instructional.sentences.count",
            len(instructional_sentences)
        )

        # --------------------------------------------------
        # 2.2️⃣ Normalize instructional content (Fix 2)
        # --------------------------------------------------
        if instructional_sentences:
            full_text = (
                full_text
                + "\n\n---\n"
                + "INSTRUCTIONAL ACTIONS (as written in the article):\n"
                + "\n".join(instructional_sentences)
            )

        # --------------------------------------------------
        # 3️⃣ Chunk (CONTENT-AGNOSTIC)
        # --------------------------------------------------
        chunks = chunk_article(full_text)
        span.set_attribute("chunks.count", len(chunks))

        if not chunks:
            return

        # --------------------------------------------------
        # 4️⃣ Common metadata (FILTERABLE)
        # --------------------------------------------------
        base_metadata = {
            "article_id": article_id,
            "short_description": short_desc,
            "knowledge_base": parsed_pdf.get("knowledge_base"),
            "category": parsed_pdf.get("category"),
            "author": parsed_pdf.get("author"),
        }

        # --------------------------------------------------
        # 5️⃣ Embed + store
        # --------------------------------------------------
        for idx, chunk in enumerate(chunks):
            embedding = embed_text(chunk)

            add_chunk(
                content=chunk,
                embedding=embedding,
                metadata={
                    **base_metadata,
                    "chunk_id": str(uuid4()),
                    "chunk_index": idx,
                    "has_instructions": any(
                        s in chunk for s in instructional_sentences
                    )
                }
            )
