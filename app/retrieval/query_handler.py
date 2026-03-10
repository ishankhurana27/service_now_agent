# def infer_query_intent(query: str) -> str:
#     if "sql" in query.lower() or "query" in query.lower():
#         return "SQL"
#     return "TEXT"

from opentelemetry import trace
tracer = trace.get_tracer(__name__)

def infer_query_intent(query: str) -> str:
    with Span("infer_query_intent") as span:
        lowered = query.lower()

        if "sql" in lowered or "query" in lowered:
            intent = "SQL"
        else:
            intent = "TEXT"

        # 🔍 Log decision (NO behavior change)
        span.log({
            "query": query,
            "detected_intent": intent
        })

        return intent
