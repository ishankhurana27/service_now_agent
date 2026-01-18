from openai import AzureOpenAI
from app.config import *

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_EMBEDDING_API_VERSION,
)

def embed_text(text: str) -> list:
    response = client.embeddings.create(
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
    )
    return response.data[0].embedding
