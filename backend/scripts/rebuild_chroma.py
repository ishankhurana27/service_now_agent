# scripts/rebuild_chroma.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ingestion.pdf_loader import load_all_pdfs
from app.core.pipeline import run_pipeline

pdfs = load_all_pdfs("data/pdfs")

for pdf in pdfs:
    run_pipeline({
        "article_id": pdf["file_name"],
        "short_description": "",
        "knowledge_base": "",
        "category": "",
        "author": "",
        "raw_text": pdf["raw_text"]
    })

print("✅ Chroma DB rebuilt successfully")
