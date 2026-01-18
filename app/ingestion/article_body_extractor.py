import re

START_MARKERS = [
    "Short Description",
    "Issue:",
    "Incident:",
    "Problem:",
    "Analysis:"
]

# ❌ Removed "ServiceNow Service Management" from here
END_MARKERS = [
    "Meta:",
    "Wiki:",
    "Feedback",
    "Approvals",
    "Article Versions",
    "Related Articles",
    "Related Catalog Items"
]

# Page noise patterns (DO NOT end article)
PAGE_NOISE_PATTERNS = [
    re.compile(r"servicenow service management", re.IGNORECASE),
    re.compile(r"https?://.*servicenow", re.IGNORECASE),
    re.compile(r"^\s*\d+/\d+\s*$"),            # 1/3, 2/3
    re.compile(r"\d{1,2}/\d{1,2}/\d{2,4}"),    # timestamps
]


def is_page_noise(line: str) -> bool:
    return any(p.search(line) for p in PAGE_NOISE_PATTERNS)


def extract_article_body(parsed_pdf: dict) -> str:
    raw_text = parsed_pdf.get("article_body", "")
    lines = raw_text.splitlines()

    start_idx = None
    end_idx = len(lines)

    # -----------------------------
    # Find START of article body
    # -----------------------------
    for i, line in enumerate(lines):
        if any(m.lower() in line.lower() for m in START_MARKERS):
            start_idx = i
            break

    if start_idx is None:
        return ""

    # -----------------------------
    # Find END of article body
    # (ignore page noise)
    # -----------------------------
    for i in range(start_idx + 1, len(lines)):
        line = lines[i]

        if is_page_noise(line):
            continue

        if any(m.lower() in line.lower() for m in END_MARKERS):
            end_idx = i
            break

    article_lines = []

    for line in lines[start_idx:end_idx]:
        if is_page_noise(line):
            continue
        article_lines.append(line)

    return "\n".join(article_lines).strip()
