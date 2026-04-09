from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "AI Interview Prep - FastAPI Service"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8001
    
    hf_model_name: str = "facebook/bart-large-cnn"
    whisper_model: str = "base"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
