import os
import uuid
from typing import Dict

from fastapi import APIRouter, HTTPException

from app.api.schemas import IngestResponse, QueryRequest, QueryResponse
from app.ingestion.pdf_loader import load_pdf
from app.core.pipeline import run_pipeline

from app.embeddings.embedder import embed_text
from app.vector_store.chroma_store import query_chunks

from app.llm.azure_llm import llm_complete
from app.processing.intent_classifier import detect_intent_llm
from app.prompts.rag_prompts import SQL_PROMPT, TEXT_PROMPT

from opentelemetry import trace


# --------------------------------------------------
# Setup
# --------------------------------------------------
tracer = trace.get_tracer(__name__)
router = APIRouter()

# 🔒 session_id → article_id
SESSION_STORE: Dict[str, str] = {}


# --------------------------------------------------
# INGEST PDFs
# --------------------------------------------------
@router.post("/ingest", response_model=IngestResponse)
def ingest_pdfs():
    with tracer.start_as_current_span("ingest_request"):

        pdf_dir = "data/pdfs"
        if not os.path.exists(pdf_dir):
            raise HTTPException(status_code=500, detail="PDF directory not found")

        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
        chunks_created = 0

        for pdf_file in pdf_files:
            with tracer.start_as_current_span("pdf_ingestion"):
                raw_text = load_pdf(os.path.join(pdf_dir, pdf_file))

                run_pipeline({
                    "article_id": pdf_file,
                    "short_description": "",
                    "knowledge_base": "",
                    "category": "",
                    "author": "",
                    "raw_text": raw_text
                })

                chunks_created += 1

        return IngestResponse(
            pdfs_ingested=len(pdf_files),
            chunks_created=chunks_created
        )


# --------------------------------------------------
# RAG QUERY
# --------------------------------------------------
@router.post("/rag/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):

    query = request.query.strip()
    session_id = request.session_id or str(uuid.uuid4())
    if request.reset_session and session_id in SESSION_STORE:
        SESSION_STORE.pop(session_id, None)

    with tracer.start_as_current_span("rag_query") as span:

        span.set_attribute("session.id", session_id)
        span.set_attribute("query.text", query)

        # 1️⃣ LLM-based intent detection (TEXT | SQL)
        intent = detect_intent_llm(query, llm_complete)
        span.set_attribute("intent", intent)

        # 2️⃣ Embed query
        query_embedding = embed_text(query)

        # --------------------------------------------------
        # 3️⃣ ARTICLE SELECTION (LOCK PER SESSION)
        # --------------------------------------------------
        if session_id in SESSION_STORE:
            article_id = SESSION_STORE[session_id]
            span.set_attribute("article.locked", True)
        else:
            results = query_chunks(query_embedding, n_results=10)
            metadatas = results.get("metadatas", [[]])[0]

            if not metadatas:
                raise HTTPException(
                    status_code=404,
                    detail="No relevant article found"
                )

            article_id = metadatas[0]["article_id"]
            SESSION_STORE[session_id] = article_id
            span.set_attribute("article.locked", False)

        span.set_attribute("article.id", article_id)

        # --------------------------------------------------
        # 4️⃣ EXPAND FULL ARTICLE (ALL CHUNKS)
        # --------------------------------------------------
        expanded = query_chunks(
            query_embedding=query_embedding,  # required by Chroma
            article_id=article_id,
            n_results=200
        )

        documents = expanded.get("documents", [[]])[0]
        metadatas = expanded.get("metadatas", [[]])[0]

# Pair chunks with chunk_index
        paired = list(zip(documents, metadatas))

# Sort by original article order
        paired.sort(key=lambda x: x[1].get("chunk_index", 0))

# Extract ordered chunks
        article_chunks = [doc for doc, _ in paired]


        if not article_chunks:
            raise HTTPException(
                status_code=500,
                detail="Article chunks missing after expansion"
            )

        full_article_content = "\n\n".join(article_chunks)

        # --------------------------------------------------
        # 5️⃣ BUILD STRICT PROMPT
        # --------------------------------------------------
        if intent == "SQL":
            prompt = SQL_PROMPT.format(content=full_article_content)
        else:
            prompt = TEXT_PROMPT.format(
                question=query,
                content=full_article_content
            )
        # --------------------------------------------------
        # 6️⃣ LLM ANSWER (STRICT, NO HALLUCINATION)
        # --------------------------------------------------
        llm_result = llm_complete(prompt)

        answer_text = llm_result["text"].strip()

        answer_text += (
            "\n\n---\n"
            "Do you want to start a new session and search another article?\n"
            "Reply with **Yes** to reset, or continue asking questions to stay on this article."
        )

        return QueryResponse(
            answer=answer_text,
            article_id=article_id,
            intent=intent,
            session_id=session_id
        )

