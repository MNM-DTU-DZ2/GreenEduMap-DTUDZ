#!/usr/bin/env python3
"""
GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
Copyright (C) 2025 DTU-DZ2 Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

"""
Weather model - OpenData compliant
"""

from datetime import datetime
from uuid import uuid4

from geoalchemy2 import Geography
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..base import Base


class Weather(Base):
    """
    Weather data from OpenWeather API
    """

    __tablename__ = "weather"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Location
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
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
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Weather(id={self.id}, temp={self.temperature}, city={self.city_name})>"
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "location": (
                {
                    "type": "Point",
                    "coordinates": [self.location.longitude, self.location.latitude],
                }
                if self.location
                else None
            ),
            "city_name": self.city_name,
            "temperature": float(self.temperature) if self.temperature else None,
            "feels_like": float(self.feels_like) if self.feels_like else None,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "wind": {
                "speed": float(self.wind_speed) if self.wind_speed else None,
                "direction": self.wind_direction,
            },
            "weather": {
                "main": self.weather_main,
                "description": self.weather_description,
                "icon": self.weather_icon,
            },
            "observation_time": (
                self.observation_time.isoformat() if self.observation_time else None
            ),
        }
