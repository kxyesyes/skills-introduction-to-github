import os
from pydantic import BaseModel


class AppConfig(BaseModel):
    provider: str = os.getenv("PROVIDER", "ollama")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_api_base: str | None = os.getenv("OPENAI_API_BASE")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    admet_api_url: str | None = os.getenv("ADMET_API_URL")
    reaction_api_url: str | None = os.getenv("REACTION_API_URL")
    retro_api_url: str | None = os.getenv("RETRO_API_URL")

    serpapi_key: str | None = os.getenv("SERPAPI_API_KEY")

    # System prompt customization
    system_prompt: str = os.getenv("SYSTEM_PROMPT", "").strip() or (
        "You are PharmAgent, a senior pharmaceutical chemistry expert."
    )


CONFIG = AppConfig()

