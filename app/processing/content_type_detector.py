import re
from app.core.constants import TEXT_ONLY, SQL_ONLY, MIXED



SQL_HINTS = re.compile(r"\b(SELECT|UPDATE|DELETE|INSERT|FROM|WHERE|JOIN)\b", re.I)

def detect_content_type(text: str) -> str:
    has_sql = bool(SQL_HINTS.search(text))
    has_text = bool(re.search(r"[a-zA-Z]{3,}", text))

    if has_sql and has_text:
        return MIXED
    if has_sql:
        return SQL_ONLY
    return TEXT_ONLY
