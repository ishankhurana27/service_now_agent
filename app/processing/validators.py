import re

SQL_REGEX = re.compile(r"\b(SELECT|UPDATE|DELETE|INSERT|FROM|WHERE|JOIN)\b", re.I)

CONFIDENCE_THRESHOLD = 0.75

def sql_confidence_score(text: str) -> float:
    tokens = len(text.split())
    sql_hits = len(SQL_REGEX.findall(text))
    if tokens == 0:
        return 0.0
    return min(sql_hits / tokens * 5, 1.0)

def is_safe_sql(text: str) -> bool:
    return sql_confidence_score(text) >= CONFIDENCE_THRESHOLD

def is_safe_text(text: str) -> bool:
    return not SQL_REGEX.search(text)
