"""
Configuration for API Gateway
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """API Gateway settings"""
    
    # Gateway Info
    APP_NAME: str = "GreenEduMap - API Gateway"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Service URLs
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    ENVIRONMENT_SERVICE_URL: str = "http://localhost:8007"
    RESOURCE_SERVICE_URL: str = "http://localhost:8000"
    EDUCATION_SERVICE_URL: str = "http://localhost:8008"
    AI_SERVICE_URL: str = "http://localhost:8006"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
    ]
    
    # Rate Limiting
    REDIS_URL: str = "redis://localhost:6379/0"
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Message Broker
    RABBITMQ_URL: str = "amqp://admin:admin123@localhost:5672/greenedumap"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
