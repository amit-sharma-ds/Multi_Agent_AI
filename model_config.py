import os

from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat


DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"
DEFAULT_OLLAMA_MODEL = "llama3.2:3b"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


def build_model(role: str, max_tokens: int):
    provider = os.getenv(f"{role.upper()}_PROVIDER", os.getenv("LLM_PROVIDER", "groq")).lower()

    if provider == "ollama":
        return Ollama(
            id=os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL),
            options={"num_predict": max_tokens},
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        )

    if provider == "groq":
        from agno.models.groq import Groq

        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY is missing. Add a valid Groq key to .env.")

        return Groq(id=os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL), max_tokens=max_tokens, timeout=60)

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is missing. Add a valid OpenAI key to .env.")

        return OpenAIChat(
            id=os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
            max_completion_tokens=max_tokens,
            timeout=60,
        )

    raise ValueError(
        f"Unsupported provider '{provider}'. Use 'openai', 'groq', or 'ollama'."
    )
