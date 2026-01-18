import os
import uuid
from typing import Dict
import sqlparse

from fastapi import APIRouter, HTTPException

from app.api.schemas import IngestResponse, QueryRequest, QueryResponse

# -------------------------
# EXISTING PROJECT IMPORTS
# -------------------------
from app.ingestion.pdf_loader import load_pdf
from app.core.pipeline import run_pipeline

from app.embeddings.embedder import embed_text
from app.vector_store.chroma_store import query_chunks
from app.retrieval.cross_encoder_reranker import rerank_chunks

from app.core.constants import CHUNK_TEXT, CHUNK_SQL

# 👉 existing LLM client (already used elsewhere in project)
from app.llm.azure_llm import llm_complete


# -------------------------
# ROUTER
# -------------------------
router = APIRouter()

# -------------------------
# IN-MEMORY SESSION STORE
# session_id -> article_id
# -------------------------
SESSION_STORE: Dict[str, str] = {}

# -------------------------
# SQL FORMATTER
# -------------------------
def format_sql(sql_chunks):
    formatted = []
    for sql in sql_chunks:
        formatted.append(
            sqlparse.format(
                sql,
                reindent=True,
                keyword_case="upper"
            )
        )
    return "\n\n".join(formatted)

# -------------------------
# LLM CONVERSATIONAL FORMATTER (NEW)
# -------------------------
def make_conversational(answer: str, intent: str) -> str:
    """
    Uses LLM ONLY to explain the answer conversationally.
    SQL is preserved and appended unchanged.
    """

    if intent == CHUNK_SQL:
        system_prompt = (
            "You are a senior database support engineer.\n"
            "Explain what the SQL scripts do in clear, simple language.\n"
            "Explain where they should be executed (e.g. application DB, prod/non-prod).\n"
            "Do NOT rewrite, remove, or modify the SQL.\n"
            "Your output must contain ONLY the explanation."
        )

        prompt = f"""
{system_prompt}

SQL SCRIPTS:
{answer}
"""

        explanation = llm_complete(prompt).strip()

        # ✅ append SQL back unchanged
        return (
            f"{explanation}\n\n"
            f"-----------------------------\n"
            f"SQL Scripts (execute as-is):\n"
            f"{answer}"
        )

    # ---------------- TEXT INTENT ----------------
    else:
        system_prompt = (
            "You are a ServiceNow support assistant.\n"
            "Rewrite the content clearly and conversationally.\n"
            "Do NOT add new facts or remove important details."
        )

        prompt = f"""
{system_prompt}

CONTENT:
{answer}
"""

        return llm_complete(prompt).strip()


# -------------------------
# INTENT DETECTION (CLI MATCH)
# -------------------------
def detect_intent(query: str, has_context: bool):
    if not has_context:
        return CHUNK_TEXT

    sql_keywords = ["sql", "query", "select", "update", "insert", "delete", "script"]
    return CHUNK_SQL if any(k in query.lower() for k in sql_keywords) else CHUNK_TEXT

# =========================================================
# POST /ingest
# =========================================================
@router.post("/ingest", response_model=IngestResponse)
def ingest_pdfs():
    pdf_dir = "data/pdfs"

    if not os.path.exists(pdf_dir):
        raise HTTPException(status_code=500, detail="PDF directory not found")

    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    if not pdf_files:
        return IngestResponse(pdfs_ingested=0, chunks_created=0)

    chunks_created = 0

    for pdf_file in pdf_files:
        try:
            raw_text = load_pdf(os.path.join(pdf_dir, pdf_file))

            parsed_pdf = {
                "article_id": pdf_file,
                "short_description": "",
                "knowledge_base": "",
                "category": "",
                "author": "",
                "raw_text": raw_text
            }

            run_pipeline(parsed_pdf)
            chunks_created += 1

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to ingest {pdf_file}: {str(e)}"
            )

    return IngestResponse(
        pdfs_ingested=len(pdf_files),
        chunks_created=chunks_created
    )

# =========================================================
# POST /rag/query
# =========================================================
@router.post("/rag/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    query_text = request.query.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # ----------------------------------
    # Session handling
    # ----------------------------------
    session_id = request.session_id or str(uuid.uuid4())
    locked_article_id = SESSION_STORE.get(session_id)

    # ----------------------------------
    # Detect intent
    # ----------------------------------
    intent = detect_intent(query_text, bool(locked_article_id))

    # ----------------------------------
    # Embed query
    # ----------------------------------
    query_embedding = embed_text(query_text)

    # =====================================================
    # FIRST QUERY → RETRIEVE + RERANK + LOCK ARTICLE
    # =====================================================
    if locked_article_id is None:
        results = query_chunks(
            query_embedding,
            intent,
            n_results=30
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        if not docs:
            return QueryResponse(
                answer="No relevant information found.",
                article_id="",
                intent=intent,
                session_id=session_id
            )

        reranked = rerank_chunks(query_text, docs, metas, top_k=10)

        locked_article_id = reranked[0][1]["article_id"]
        SESSION_STORE[session_id] = locked_article_id

        final_results = [
            (doc, meta)
            for doc, meta in reranked
            if meta["article_id"] == locked_article_id
        ]

    # =====================================================
    # FOLLOW-UP → SAME ARTICLE ONLY
    # =====================================================
    else:
        results = query_chunks(
            query_embedding,
            intent,
            article_id=locked_article_id,
            n_results=20
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        if not docs:
            return QueryResponse(
                answer="No relevant information found in this article.",
                article_id=locked_article_id,
                intent=intent,
                session_id=session_id
            )

        final_results = list(zip(docs, metas))

    # =====================================================
    # ANSWER CONSTRUCTION (RAW)
    # =====================================================
    if intent == CHUNK_SQL:
        sql_chunks = [doc for doc, _ in final_results]
        raw_answer = format_sql(sql_chunks)
    else:
        raw_answer = "\n\n".join(doc for doc, _ in final_results[:3])

    # =====================================================
    # 🔥 LLM POST-PROCESSING (PRESENTATION ONLY)
    # =====================================================
    final_answer = make_conversational(raw_answer, intent)

    return QueryResponse(
        answer=final_answer.strip(),
        article_id=locked_article_id,
        intent=intent,
        session_id=session_id
    )
