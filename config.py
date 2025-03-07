from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    EMAIL_HOST: str
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"  # Default model
    DEBUG: bool = True
    CHECK_INTERVAL: int = 10  # Default to 60 seconds if not set
    DB_HOST: str
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    OCR_PROJECT_ID: str
    OCR_LOCATION: str
    OCR_PROCESSOR_VERSION: str
    GOOGLE_APPLICATION_CREDENTIALS: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Cache settings for better performance."""
    return Settings()
