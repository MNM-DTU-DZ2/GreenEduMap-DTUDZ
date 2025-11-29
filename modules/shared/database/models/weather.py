"""
Weather model - OpenData compliant
"""

from sqlalchemy import Column, String, Numeric, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from geoalchemy2 import Geography
from datetime import datetime
from uuid import uuid4

from ..base import Base


class Weather(Base):
    """
    Weather data from OpenWeather API
    """
    __tablename__ = "weather"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Location
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    city_name = Column(String(255), nullable=True)
    
    # Weather conditions
    temperature = Column(Numeric(5, 2), nullable=True)  # Celsius
    feels_like = Column(Numeric(5, 2), nullable=True)
    humidity = Column(Integer, nullable=True)  # Percentage
    pressure = Column(Integer, nullable=True)  # hPa
    wind_speed = Column(Numeric(5, 2), nullable=True)  # m/s
    wind_direction = Column(Integer, nullable=True)  # Degrees
    clouds = Column(Integer, nullable=True)  # Percentage
    visibility = Column(Integer, nullable=True)  # Meters
    
    # Weather description
    weather_main = Column(String(50), nullable=True)  # e.g., "Clear", "Rain"
    weather_description = Column(String(255), nullable=True)
    weather_icon = Column(String(10), nullable=True)
    
    # Rainfall/Snow
    rain_1h = Column(Numeric(10, 2), nullable=True)  # mm
    rain_3h = Column(Numeric(10, 2), nullable=True)
    snow_1h = Column(Numeric(10, 2), nullable=True)
    snow_3h = Column(Numeric(10, 2), nullable=True)
    
    # OpenData fields
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String(500), nullable=True)
    ngsi_ld_uri = Column(String(500), nullable=True)
    
    # Source
    source = Column(String(50), default="openweather", nullable=False)
    
    # Temporal
    observation_time = Column(DateTime(timezone=True), nullable=False, index=True)
    sunrise = Column(DateTime(timezone=True), nullable=True)
    sunset = Column(DateTime(timezone=True), nullable=True)
    
    # Extensibility
    meta_data = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Weather(id={self.id}, temp={self.temperature}, city={self.city_name})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "location": {
                "type": "Point",
                "coordinates": [self.location.longitude, self.location.latitude]
            } if self.location else None,
            "city_name": self.city_name,
            "temperature": float(self.temperature) if self.temperature else None,
            "feels_like": float(self.feels_like) if self.feels_like else None,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "wind": {
                "speed": float(self.wind_speed) if self.wind_speed else None,
                "direction": self.wind_direction
            },
            "weather": {
                "main": self.weather_main,
                "description": self.weather_description,
                "icon": self.weather_icon
            },
            "observation_time": self.observation_time.isoformat() if self.observation_time else None,
        }
