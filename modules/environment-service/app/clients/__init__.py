"""
External API clients
"""

from .openaq import openaq_client, OpenAQClient
from .openweather import openweather_client, OpenWeatherClient

__all__ = [
    "openaq_client",
    "openweather_client",
    "OpenAQClient",
    "OpenWeatherClient",
]
