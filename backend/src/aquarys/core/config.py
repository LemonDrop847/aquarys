"""Configuration settings for AQUARYS backend."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SERVICE_NAME: str = "aquarys"
    VERSION: str = "0.1.0"
    APP_MODE: str = Field(default="demo", description="demo, live, or test")

    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./aquarys.db",
        description="Database connection URL (PostgreSQL+asyncpg or sqlite+aiosqlite)",
    )

    # OAH External API
    OAH_BASE_URL: str = Field(
        default="https://api.enora-oah.eu",
        description="OneAquaHealth base API URL",
    )
    OAH_API_KEY: str = Field(default="", description="OAH API key if required")

    # LLM Providers
    LLM_PROVIDER: str = Field(default="demo", description="gemini, ollama, openai, or demo")
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434", description="Ollama API base URL"
    )
    OLLAMA_MODEL: str = Field(default="llama3.2", description="Ollama model name")
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key if provider is openai")
    OPENAI_BASE_URL: str = Field(default="https://api.openai.com/v1", description="OpenAI base URL")

    # CORS
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated allowed origins",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
