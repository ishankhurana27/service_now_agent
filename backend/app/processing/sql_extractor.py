import re

SQL_START = re.compile(
    r"^\s*(select|update|insert|delete|merge|create|alter|drop|with)\b",
    re.IGNORECASE
)

def extract_full_sql(article_chunks: list[str]) -> str:
    """
    Deterministically extract FULL SQL block
    across chunks in correct order.
    """

    sql_lines = []
    in_sql = False

    for chunk in article_chunks:
        for line in chunk.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            # SQL start
            if SQL_START.match(stripped):
                in_sql = True

            if in_sql:
                sql_lines.append(line)

    return "\n".join(sql_lines).strip()
