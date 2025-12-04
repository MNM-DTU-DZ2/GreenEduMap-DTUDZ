"""
AI Service Configuration
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """AI Service Settings"""
    
    # Service Info
    APP_NAME: str = "GreenEduMap - AI Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/greenedumap"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://admin:admin123@localhost:5672/greenedumap"
    
    # ML Parameters
    CLUSTERING_N_CLUSTERS: int = 3  # Green, Yellow, Red zones
    PREDICTION_FORECAST_DAYS: int = 7
    CORRELATION_MIN_SAMPLES: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

