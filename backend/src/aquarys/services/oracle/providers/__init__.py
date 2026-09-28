"""Oracle reasoning provider factory."""

from aquarys.core.config import settings
from aquarys.services.oracle.providers.base import LLMProvider
from aquarys.services.oracle.providers.demo import DemoProvider
from aquarys.services.oracle.providers.gemini import GeminiProvider
from aquarys.services.oracle.providers.ollama import OllamaProvider


def get_llm_provider(provider_type: str | None = None) -> LLMProvider:
    """Factory to instantiate configured LLM provider."""
    provider = provider_type or settings.llm_provider
    if provider == "gemini":
        return GeminiProvider()
    elif provider == "ollama":
        return OllamaProvider()
    return DemoProvider()
