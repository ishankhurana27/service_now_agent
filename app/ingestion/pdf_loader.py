from pypdf import PdfReader
from pathlib import Path

def load_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def load_all_pdfs(pdf_dir: str):
    pdfs = []
    for pdf in Path(pdf_dir).glob("*.pdf"):
        pdfs.append({
            "file_name": pdf.name,
            "raw_text": load_pdf(str(pdf))
        })
    return pdfs
