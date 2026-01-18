from uuid import uuid4

from app.ingestion.article_body_extractor import extract_article_body
from app.processing.content_type_detector import detect_content_type
from app.processing.mixed_content_splitter import split_text_and_sql
from app.embeddings.embedder import embed_text
from app.vector_store.chroma_store import add_chunk
from app.core.constants import CHUNK_TEXT, CHUNK_SQL, MIXED, SQL_ONLY


def run_pipeline(parsed_pdf: dict):
    print("\n---- PIPELINE START ----")
    print("Article:", parsed_pdf["article_id"])

    article_body = extract_article_body(parsed_pdf)
    content_type = detect_content_type(article_body)

    print("Detected content type:", content_type)

    base_metadata = {
        "article_id": parsed_pdf["article_id"],
        "short_description": parsed_pdf["short_description"],
        "knowledge_base": parsed_pdf["knowledge_base"],
        "category": parsed_pdf["category"],
        "author": parsed_pdf["author"],
    }

    # ======================================================
    # 🔑 STEP 1: ADD SHORT DESCRIPTION AS ITS OWN CHUNK
    # ======================================================
    short_desc = parsed_pdf.get("short_description", "").strip()

    if short_desc:
        print("Adding SHORT DESCRIPTION chunk")

        add_chunk(
            embed_text(short_desc),
            short_desc,
            {
                **base_metadata,
                "chunk_type": CHUNK_TEXT,
                "chunk_id": str(uuid4()),
                "chunk_role": "SHORT_DESCRIPTION"  # optional but useful
            }
        )

    # ======================================================
    # NON-MIXED CASE
    # ======================================================
    if content_type != MIXED:
        chunk_type = CHUNK_SQL if content_type == SQL_ONLY else CHUNK_TEXT
        print("Adding NON-MIXED BODY chunk:", chunk_type)

        metadata = {
            **base_metadata,
            "chunk_type": chunk_type,
            "chunk_id": str(uuid4())
        }

        if chunk_type == CHUNK_SQL:
            metadata["sql_order"] = 0

        add_chunk(
            embed_text(article_body),
            article_body,
            metadata
        )

        print("✅ Chunk added")
        return

    # ======================================================
    # MIXED CASE
    # ======================================================
    print("Splitting mixed content via LLM")
    result = split_text_and_sql(article_body)

    # TEXT PARTS
    for text in result.get("text_parts", []):
        if not text.strip():
            continue

        print("Adding TEXT sub-chunk")

        add_chunk(
            embed_text(text),
            text,
            {
                **base_metadata,
                "chunk_type": CHUNK_TEXT,
                "chunk_id": str(uuid4())
            }
        )

    # SQL PARTS (ORDER PRESERVED)
    for idx, sql in enumerate(result.get("sql_parts", [])):
        if not sql.strip():
            continue

        print(f"Adding SQL sub-chunk (order={idx})")

        add_chunk(
            embed_text(sql),
            sql,
            {
                **base_metadata,
                "chunk_type": CHUNK_SQL,
                "chunk_id": str(uuid4()),
                "sql_order": idx
            }
        )

    print("---- PIPELINE END ----")
