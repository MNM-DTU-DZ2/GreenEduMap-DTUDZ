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

