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
OpenWeather API client
"""

import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class OpenWeatherClient:
    """Client for OpenWeather API"""
    
    def __init__(self):
        self.base_url = settings.OPENWEATHER_API_URL
        self.api_key = settings.OPENWEATHER_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def get_current_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Get current weather for a location
        
        Args:
            latitude: Latitude
            longitude: Longitude
            
        Returns:
            Weather data dictionary or None
        """
        if not self.api_key:
            logger.warning("OpenWeather API key not configured")
            return None
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            logger.info(f"Fetching current weather for ({latitude}, {longitude})")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self.parse_current_weather(data, latitude, longitude)
            
        except httpx.HTTPError as e:
            logger.error(f"OpenWeather API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching weather: {e}")
            return None
    
    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 5
    ) -> Optional[Dict[str, Any]]:
        """
        Get weather forecast (5 days / 3 hour intervals)
        
        Args:
            latitude: Latitude
            longitude: Longitude
            days: Number of days (max 5 for free tier)
            
        Returns:
            Forecast data or None
        """
        if not self.api_key:
            logger.warning("OpenWeather API key not configured")
            return None
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
                "units": "metric"
            }
            
            logger.info(f"Fetching forecast for ({latitude}, {longitude})")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            return None
    
    def parse_current_weather(
        self,
        raw_data: Dict[str, Any],
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """
        Parse OpenWeather current weather data
        
        Args:
            raw_data: Raw weather data from API
            latitude: Latitude
            longitude: Longitude
            
        Returns:
            Parsed weather dictionary
        """
        main = raw_data.get("main", {})
        wind = raw_data.get("wind", {})
        clouds = raw_data.get("clouds", {})
        weather = raw_data.get("weather", [{}])[0]
        sys = raw_data.get("sys", {})
        rain = raw_data.get("rain", {})
        snow = raw_data.get("snow", {})
        
        return {
            "latitude": latitude,
            "longitude": longitude,
            "city_name": raw_data.get("name"),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "wind_speed": wind.get("speed"),
            "wind_direction": wind.get("deg"),
            "clouds": clouds.get("all"),
            "visibility": raw_data.get("visibility"),
            "weather_main": weather.get("main"),
            "weather_description": weather.get("description"),
            "weather_icon": weather.get("icon"),
            "rain_1h": rain.get("1h"),
            "rain_3h": rain.get("3h"),
            "snow_1h": snow.get("1h"),
            "snow_3h": snow.get("3h"),
            "observation_time": datetime.utcnow(),
            "sunrise": datetime.fromtimestamp(sys.get("sunrise")) if sys.get("sunrise") else None,
            "sunset": datetime.fromtimestamp(sys.get("sunset")) if sys.get("sunset") else None,
            "source": "openweather"
        }


# Global client instance
openweather_client = OpenWeatherClient()
