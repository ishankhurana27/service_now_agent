def infer_query_intent(query: str) -> str:
    if "sql" in query.lower() or "query" in query.lower():
        return "SQL"
    return "TEXT"
