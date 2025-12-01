"""
Shared database models for OpenData-first architecture
"""

from .air_quality import AirQuality
from .catalog import DataCatalog
from .resource import RescueCenter, Resource
from .school import School
from .weather import Weather

__all__ = [
    "AirQuality",
    "Weather",
    "School",
    "Resource",
    "RescueCenter",
    "DataCatalog",
]
