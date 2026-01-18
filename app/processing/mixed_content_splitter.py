import re


SQL_START_PATTERN = re.compile(
    r"^\s*(select|update|insert|delete|merge|with)\b",
    re.IGNORECASE
)

SQL_COMMENT_PATTERN = re.compile(r"^\s*--")

SECTION_BOUNDARY_PATTERN = re.compile(
    r"^\s*(meta:|wiki:|feedback:|knowledge:|related articles)",
    re.IGNORECASE
)

PAGE_NOISE_PATTERN = re.compile(
    r"^\s*(\d+/\d+|servicenow service management|\d{1,2}/\d{1,2}/\d{2,4})",
    re.IGNORECASE
)


def split_text_and_sql(article_body: str) -> dict:
    """
    FINAL ServiceNow-safe SQL extractor

    Rules:
    - ALL SQL in article body is ONE logical block
    - SQL may resume after comments, text, page breaks
    - Ignore ServiceNow headers/footers
    - Stop only at true section boundaries
    """

    lines = article_body.splitlines()

    text_parts = []
    sql_lines = []

    sql_context_started = False

    for line in lines:
        stripped = line.strip()

        # -------- IGNORE PAGE NOISE --------
        if PAGE_NOISE_PATTERN.match(stripped):
            continue

        # -------- HARD STOP --------
        if SECTION_BOUNDARY_PATTERN.match(stripped):
            break

        # -------- SQL START --------
        if SQL_START_PATTERN.match(stripped):
            sql_context_started = True
            sql_lines.append(line)
            continue

        # -------- SQL CONTEXT --------
        if sql_context_started:
            # keep everything once SQL starts
            sql_lines.append(line)
            continue

        # -------- NORMAL TEXT --------
        text_parts.append(line)

    sql_block = "\n".join(sql_lines).strip()

    return {
        "text_parts": [t for t in text_parts if t.strip()],
        "sql_parts": [sql_block] if len(sql_block.split()) > 15 else []
    }
