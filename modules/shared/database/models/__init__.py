"""
Shared database models for OpenData-first architecture
"""

from .air_quality import AirQuality
from .weather import Weather
from .school import School
from .resource import Resource, RescueCenter
from .catalog import DataCatalog

__all__ = [
    "AirQuality",
    "Weather",
    "School",
    "Resource",
    "RescueCenter",
    "DataCatalog",
]
