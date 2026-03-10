def detect_intent_llm(query: str, llm_complete):
    prompt = f"""
You are an intent classifier.

Classify the user query strictly as ONE of:
- TEXT
- SQL

Rules:
- SQL means user is asking for database queries, scripts, statements
- TEXT means explanation, steps, description, troubleshooting
- Respond with ONLY one word: TEXT or SQL

Query:
{query}
"""

    resp = llm_complete(prompt)
    return resp["text"].strip().upper()
