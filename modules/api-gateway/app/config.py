#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

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
