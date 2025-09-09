from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from .config import CONFIG


def get_chat_model(**overrides: Any) -> BaseChatModel:
    provider = overrides.get("provider", CONFIG.provider)
    if provider == "ollama":
        model = overrides.get("model", CONFIG.ollama_model)
        return ChatOllama(model=model, temperature=overrides.get("temperature", 0.2))
    # Default to OpenAI-compatible (works for Qwen if endpoint is compatible)
    api_key = overrides.get("openai_api_key", CONFIG.openai_api_key)
    base_url = overrides.get("openai_api_base", CONFIG.openai_api_base)
    model = overrides.get("model", CONFIG.openai_model)
    if api_key is None:
        raise ValueError("OPENAI_API_KEY not set for provider 'openai'.")
    return ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=overrides.get("temperature", 0.2),
    )

