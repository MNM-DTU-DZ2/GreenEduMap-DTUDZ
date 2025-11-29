"""
API Routes
"""

from .air_quality import router as air_quality_router
from .weather import router as weather_router

__all__ = ["air_quality_router", "weather_router"]
