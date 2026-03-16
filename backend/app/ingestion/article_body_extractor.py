import re


# -----------------------------
# START of Article Body
# -----------------------------
ARTICLE_BODY_START = re.compile(
    r"^\s*article\s+body\s*:\s*$",
    re.IGNORECASE
)

# -----------------------------
# TRUE END markers (ServiceNow)
# -----------------------------
ARTICLE_BODY_END = re.compile(
    r"^\s*(meta:|wiki:|affected products|feedback|knowledge related)\s*$",
    re.IGNORECASE
)

# -----------------------------
# Noise patterns (DO NOT STOP)
# -----------------------------
PAGE_HEADER_FOOTER = re.compile(
    r"(servicenow service management|\d{1,2}/\d{1,2}/\d{2,4}|\d+:\d+\s*(am|pm))",
    re.IGNORECASE
)

URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)


def extract_article_body(parsed_pdf: dict) -> str:
    """
    Extract ONLY the ServiceNow Article Body section.

    Rules:
    - Start ONLY after 'Article body:'
    - Stop ONLY at Meta / Wiki / Feedback / Affected Products
    - DO NOT stop on page breaks, dashed lines, headers, timestamps
    - Preserve SQL, email templates, steps, formatting
    """

    raw_text = parsed_pdf.get("raw_text", "")
    if not raw_text:
        return ""

    lines = raw_text.splitlines()

    in_body = False
    body_lines = []

    for line in lines:
        stripped = line.strip()

        # -----------------------------
        # Detect Article Body START
        # -----------------------------
        if not in_body:
            if ARTICLE_BODY_START.match(stripped):
                in_body = True
            continue

        # -----------------------------
        # Detect Article Body END
        # -----------------------------
        if ARTICLE_BODY_END.match(stripped):
            break

        # -----------------------------
        # Ignore obvious noise
        # -----------------------------
        if not stripped:
            body_lines.append("")  # preserve paragraph spacing
            continue

        if PAGE_HEADER_FOOTER.search(stripped):
            continue

        if URL_PATTERN.search(stripped):
            continue

        # -----------------------------
        # Keep EVERYTHING else
        # -----------------------------
        body_lines.append(line)

    return "\n".join(body_lines).strip()
