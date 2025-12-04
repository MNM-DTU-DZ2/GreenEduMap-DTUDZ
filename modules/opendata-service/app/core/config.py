"""
Configuration for OpenData Service
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "GreenEduMap - OpenData Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/greenedumap"
    
    # Base URL for generating URIs
    BASE_URL: str = "http://localhost:8009"
    DATA_BASE_URI: str = "http://greenedumap.vn/data"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Debug
    DEBUG: bool = True
    
    # Pagination
    MAX_PAGE_SIZE: int = 1000
    DEFAULT_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

