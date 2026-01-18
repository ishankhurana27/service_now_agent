from app.retrieval.cross_encoder_reranker import rerank_chunks
from app.embeddings.embedder import embed_text
from app.vector_store.chroma_store import query_chunks
from app.core.constants import CHUNK_TEXT, CHUNK_SQL


def detect_intent(user_query: str, has_context: bool):
    # First question always treated as TEXT
    if not has_context:
        return CHUNK_TEXT

    sql_keywords = ["sql", "query", "select", "update", "insert", "delete", "script"]
    for kw in sql_keywords:
        if kw in user_query.lower():
            return CHUNK_SQL

    return CHUNK_TEXT


def run_cli():
    print("\n=== ServiceNow KB Query CLI (Two-Stage Retrieval) ===")
    print("Type 'exit' to quit\n")

    last_article_id = None  # 🔒 HARD LOCK

    while True:
        user_query = input("Ask a question: ").strip()
        if user_query.lower() == "exit":
            break

        intent = detect_intent(user_query, has_context=bool(last_article_id))
        print(f"\nDetected intent: {intent}")

        embedding = embed_text(user_query)

        # ===============================
        # FIRST QUESTION → SELECT ARTICLE
        # ===============================
        if last_article_id is None:
            results = query_chunks(
                embedding,
                intent,
                n_results=30
            )

            docs = results["documents"][0]
            metas = results["metadatas"][0]

            if not docs:
                print("No results found.")
                continue

            # 🔥 CROSS-ENCODER RUNS ONLY HERE
            reranked = rerank_chunks(user_query, docs, metas, top_k=10)

            last_article_id = reranked[0][1]["article_id"]
            print(f"\n🔒 Context locked to Article: {last_article_id}")

            final_results = [
                (doc, meta)
                for doc, meta in reranked
                if meta["article_id"] == last_article_id
            ]

        # ===============================
        # FOLLOW-UP → SAME ARTICLE ONLY
        # ===============================
        else:
            results = query_chunks(
                embedding,
                intent,
                article_id=last_article_id,
                n_results=20
            )

            docs = results["documents"][0]
            metas = results["metadatas"][0]

            if not docs:
                print("No results found in this article.")
                continue

            final_results = list(zip(docs, metas))

        # ===============================
        # OUTPUT
        # ===============================
        if intent == CHUNK_TEXT:
            print("\n---- ANSWER ----\n")
            for doc, _ in final_results[:3]:
                print(doc.strip())
                print()

        elif intent == CHUNK_SQL:
            print("\n---- SQL QUERY ----\n")
            sql_chunks = sorted(
                final_results,
                key=lambda x: x[1].get("sql_order", 0)
            )
            for doc, _ in sql_chunks:
                print(doc.strip())
                print()



if __name__ == "__main__":
    run_cli()