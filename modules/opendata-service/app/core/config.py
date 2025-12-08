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

