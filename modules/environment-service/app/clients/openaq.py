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
OpenAQ API client for air quality data
"""

import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class OpenAQClient:
    """Client for OpenAQ API v2"""
    
    def __init__(self):
        self.base_url = settings.OPENAQ_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def get_latest_measurements(
        self,
        latitude: float,
        longitude: float,
        radius: int = 50000,  # 50km in meters
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get latest air quality measurements near a location
        
        Args:
            latitude: Latitude
            longitude: Longitude
            radius: Search radius in meters (max 100km)
            limit: Max results to return
            
        Returns:
            List of measurement dictionaries
        """
        try:
            url = f"{self.base_url}/latest"
            params = {
                "coordinates": f"{latitude},{longitude}",
                "radius": min(radius, 100000),  # Max 100km
                "limit": limit,
                "order_by": "distance"
            }
            
            logger.info(f"Fetching OpenAQ data for location ({latitude}, {longitude})")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            logger.info(f"Retrieved {len(results)} air quality measurements from OpenAQ")
            return results
            
        except httpx.HTTPError as e:
            logger.error(f"OpenAQ API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching OpenAQ data: {e}")
            return []
    
    async def get_measurements_by_location_name(
        self,
        location_name: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get measurements by location name
        
        Args:
            location_name: Location/city name
            limit: Max results
            
        Returns:
            List of measurements
        """
        try:
            url = f"{self.base_url}/latest"
            params = {
                "location": location_name,
                "limit": limit
            }
            
            logger.info(f"Fetching OpenAQ data for location: {location_name}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("results", [])
            
        except Exception as e:
            logger.error(f"Error fetching OpenAQ data by name: {e}")
            return []
    
    def parse_measurement(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse OpenAQ measurement data into our format
        
        Args:
            raw_data: Raw measurement from OpenAQ API
            
        Returns:
            Parsed measurement dictionary
        """
        try:
            # Extract coordinates
            coordinates = raw_data.get("coordinates", {})
            lat = coordinates.get("latitude")
            lon = coordinates.get("longitude")
            
            if not lat or not lon:
                return None
            
            # Extract measurements
            measurements = raw_data.get("measurements", [])
            measurement_dict = {}
            
            for m in measurements:
                param = m.get("parameter", "").lower()
                value = m.get("value")
                
                if param and value is not None:
                    measurement_dict[param] = float(value)
            
            # Parse date
            date_str = raw_data.get("date", {}).get("utc")
            measurement_date = datetime.fromisoformat(date_str.replace("Z", "+00:00")) if date_str else datetime.utcnow()
            
            return {
                "latitude": lat,
                "longitude": lon,
                "station_name": raw_data.get("location"),
                "measurements": measurement_dict,
                "measurement_date": measurement_date,
                "source": "openaq"
            }
            
        except Exception as e:
            logger.error(f"Error parsing OpenAQ measurement: {e}")
            return None


# Global client instance
openaq_client = OpenAQClient()
