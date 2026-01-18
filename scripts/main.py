import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app.ingestion.pdf_loader import load_all_pdfs
from app.core.pipeline import run_pipeline

pdfs = load_all_pdfs("data/pdfs")

for pdf in pdfs:
    parsed_pdf = {
        "article_id": pdf["file_name"],
        "short_description": "Extracted from metadata",
        "knowledge_base": "Logistics",
        "category": "WMS",
        "author": "Unknown",
        "article_body": pdf["raw_text"],
    }
    run_pipeline(parsed_pdf)
