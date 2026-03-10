# from openai import AzureOpenAI
# from app.config import (
#     AZURE_OPENAI_API_KEY,
#     AZURE_OPENAI_ENDPOINT,
#     AZURE_OPENAI_API_VERSION,
#     AZURE_OPENAI_MODEL_DEPLOYMENT,
#     MODEL_TEMPERATURE
# )

# _client = AzureOpenAI(
#     api_key=AZURE_OPENAI_API_KEY,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT,
#     api_version=AZURE_OPENAI_API_VERSION
# )

# def llm_complete(prompt: str) -> str:
#     response = _client.chat.completions.create(
#         model=AZURE_OPENAI_MODEL_DEPLOYMENT,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=MODEL_TEMPERATURE,
#     )

#     return response.choices[0].message.content


from openai import AzureOpenAI
from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_MODEL_DEPLOYMENT,
    MODEL_TEMPERATURE
)

# -------------------------
# Azure OpenAI Client
# -------------------------
_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)

# -------------------------
# Cost config (USD per 1K tokens)
# Adjust if you change models
# -------------------------
MODEL_COST_PER_1K = {
    "gpt-4o-mini-2024-07-18": 0.00015,
    "gpt-4o-mini": 0.00015,
}

def estimate_cost(deployment_name: str, total_tokens: int) -> float:
    cost_per_1k = MODEL_COST_PER_1K.get(deployment_name, 0.0)
    return (total_tokens / 1000) * cost_per_1k




# ======================================================
# LLM CALL (WITH TOKEN + COST METADATA)
# ======================================================
def llm_complete(prompt: str) -> dict:
    response = _client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=MODEL_TEMPERATURE,
    )

    usage = response.usage
    total_tokens = usage.total_tokens

    cost = estimate_cost(
        AZURE_OPENAI_MODEL_DEPLOYMENT,
        total_tokens
    )

    return {
        "text": response.choices[0].message.content,
        "model": AZURE_OPENAI_MODEL_DEPLOYMENT,  # IMPORTANT
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "total_tokens": total_tokens,
        "cost_usd": round(cost, 6),
    }
