"""
Configuration management for Environment Service
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Service Info
    APP_NAME: str = "GreenEduMap - Environment Service"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8007
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/greenedumap"
    
    # External APIs
    OPENAQ_API_URL: str = "https://api.openaq.org/v2"
    OPENWEATHER_API_KEY: str = ""
    OPENWEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://admin:admin123@localhost:5672/greenedumap"
    
    # MQTT (EMQX)
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_CLIENT_ID: str = "environment-service"
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Scheduler Intervals (seconds)
    FETCH_AIR_QUALITY_INTERVAL: int = 3600  # 1 hour
    FETCH_WEATHER_INTERVAL: int = 1800      # 30 minutes
    
    # Data Retention (days)
    AIR_QUALITY_RETENTION_DAYS: int = 90
    WEATHER_RETENTION_DAYS: int = 30
    
    # Alert Thresholds
    AQI_WARNING_THRESHOLD: float = 100.0  # AQI > 100 = unhealthy
    AQI_CRITICAL_THRESHOLD: float = 150.0  # AQI > 150 = very unhealthy
    
    # Default locations to fetch (Vietnam cities)
    DEFAULT_LOCATIONS: List[dict] = [
        {"name": "Da Nang", "lat": 16.0544, "lon": 108.2022},
        {"name": "Hanoi", "lat": 21.0285, "lon": 105.8542},
        {"name": "Ho Chi Minh", "lat": 10.8231, "lon": 106.6297},
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
