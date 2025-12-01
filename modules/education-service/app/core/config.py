"""
Configuration for Education Service
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Education Service settings"""
    
    # App Info
    APP_NAME: str = "GreenEduMap - Education Service"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8008
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/greenedumap"
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
