import sys
import os
from app.vector_store.chroma_store import collection

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("Total vectors stored:", collection.count())
