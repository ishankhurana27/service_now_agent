import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="sql_text_kb"
)

# -------------------------
# ADD CHUNK
# -------------------------
def add_chunk(embedding, content, metadata):
    collection.add(
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata],
        ids=[metadata["chunk_id"]],
    )


# -------------------------
# VECTOR QUERY (PRIMARY)
# -------------------------
def query_chunks(query_embedding, n_results=10, article_id=None):
    where_clause = {"article_id": article_id} if article_id else None

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_clause
    )


def fetch_chunks_by_article(article_id: str):
    """
    Fetch ALL chunks of an article WITHOUT embeddings.
    """
    return collection.get(
        where={"article_id": article_id}
    )
