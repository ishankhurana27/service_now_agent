import chromadb

# THIS is the correct persistent client
client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="sql_text_kb"
)

def add_chunk(embedding, content, metadata):
    collection.add(
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata],
        ids=[metadata["chunk_id"]],
    )

def query_chunks(query_embedding, chunk_type, n_results=10, article_id=None):
    if article_id:
        where_clause = {
            "$and": [
                {"chunk_type": chunk_type},
                {"article_id": article_id}
            ]
        }
    else:
        where_clause = {
            "chunk_type": chunk_type
        }

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_clause
    )
