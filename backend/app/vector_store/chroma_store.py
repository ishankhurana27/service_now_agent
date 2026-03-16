import chromadb

_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path="chroma_db")
        _collection = _client.get_or_create_collection(name="sql_text_kb")
    return _collection

def add_chunk(embedding, content, metadata):
    collection = get_collection()
    collection.add(
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata],
        ids=[metadata["chunk_id"]],
    )

def query_chunks(query_embedding, n_results=10, article_id=None):
    collection = get_collection()
    where_clause = {"article_id": article_id} if article_id else None
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_clause
    )

def fetch_chunks_by_article(article_id: str):
    collection = get_collection()
    return collection.get(where={"article_id": article_id})