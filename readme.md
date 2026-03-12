**ServiceNow Knowledge Base RAG System**

This project is a Retrieval-Augmented Generation (RAG) system built to answer questions from ServiceNow Knowledge Base PDFs.

**system architecture:**

PDF Knowledge Base
        │
        ▼
Article Body Extraction
        │
        ▼
Chunking
        │
        ▼
Embeddings Generation
        │
        ▼
Chroma Vector Database
        │
        ▼
User Query
        │
        ▼
Intent Detection (TEXT / SQL)
        │
        ▼
Article Retrieval
        │
        ▼
Article Reconstruction
        │
        ▼
LLM Response Generation

**Project Setup**


**1. Clone the Repository**
git clone <repository-url>
cd ServiceNow


**2. Create Virtual Environment**
Windows
python -m venv venv
venv\Scripts\activate
Mac / Linux
python -m venv venv
source venv/bin/activate


**3. Install Dependencies**
pip install -r requirements.txt

If requirements.txt is missing, install manually:

pip install fastapi uvicorn chromadb openai pypdf sqlparse


**4. Configure Environment Variables**

Create a .env file in the project root.

Example:

AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=your_deployment

These are used by:

app/llm/azure_llm.py

**5. Add Knowledge Base PDFs**

Place all KB PDFs inside:

data/pdfs/

Example:

data/pdfs/
  KB0015105.pdf
  KB0019223.pdf
  KB0020281.pdf

**6. Build the Vector Database**

This step extracts article bodies, creates chunks, generates embeddings, and stores them in ChromaDB.

Run:

python scripts/rebuild_chroma.py

This will create the vector database inside:

vector_store/chroma_db/


**7. Start the API Server**

Run:

uvicorn app.api.main:app --reload

Server will start at:

http://127.0.0.1:8000

**8. Test the API**

Open Swagger UI:

http://127.0.0.1:8000/docs

Use the endpoint:

POST /rag/query

Example request:

{
  "query": "Why is ALDATAPROD-disloadpso failing with ORA-00054?",
  "session_id": "demo1"
}


**System Workflow**

PDF
 ↓
Extract Article Body
 ↓
Chunk Article
 ↓
Generate Embeddings
 ↓
Store in ChromaDB
 ↓
Query → Retrieve → LLM → Response


**Updating Knowledge Base**

If new PDFs are added:

Place them in data/pdfs

Then Rebuild the database:

python scripts/rebuild_chroma.py

**Important Features**

Session-based article locking

Strict SQL extraction

No hallucinated answers

Uses short description verification to select correct article

Preserves SQL blocks exactly as written