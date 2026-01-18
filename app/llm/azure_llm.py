from openai import AzureOpenAI
from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_MODEL_DEPLOYMENT,
    MODEL_TEMPERATURE
)

_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)

def llm_complete(prompt: str) -> str:
    response = _client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=MODEL_TEMPERATURE,
    )

    return response.choices[0].message.content
