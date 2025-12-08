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
Public OpenData API endpoints (no authentication required)
"""

from fastapi import APIRouter, Query, HTTPException
import httpx
import logging

from ..config import settings

router = APIRouter(prefix="/api/open-data", tags=["OpenData"])
logger = logging.getLogger(__name__)


# ============================================
# Air Quality Endpoints
# ============================================

@router.get("/air-quality")
async def get_public_air_quality(limit: int = Query(100, ge=1, le=1000)):
    """Get public air quality data"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.ENVIRONMENT_SERVICE_URL}/api/v1/air-quality/latest"
            response = await client.get(url, params={"limit": limit}, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error proxying to environment service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/air-quality/location")
async def get_air_quality_by_location(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: int = Query(50, ge=1, le=200)
):
    """Get air quality near a location"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.ENVIRONMENT_SERVICE_URL}/api/v1/air-quality/location"
            params = {"lat": lat, "lon": lon, "radius": radius}
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching air quality: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching air quality: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# ============================================
# Weather Endpoints
# ============================================

@router.get("/weather/current")
async def get_public_current_weather(
    city: str = Query(None),
    lat: float = Query(None, ge=-90, le=90),
    lon: float = Query(None, ge=-180, le=180)
):
    """Get current weather (public) - accepts either city or lat/lon"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.ENVIRONMENT_SERVICE_URL}/api/v1/weather/current"
            params = {}
            
            # If lat/lon provided, use them with fetch_new
            if lat is not None and lon is not None:
                params["lat"] = lat
                params["lon"] = lon
                params["fetch_new"] = "true"
            elif city:
                # For city, we need to geocode first or use a default location
                # For now, use Da Nang coordinates
                params["lat"] = 16.0678
                params["lon"] = 108.2208
                params["fetch_new"] = "true"
            else:
                raise HTTPException(status_code=400, detail="Either city or lat/lon required")
                
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching weather: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/weather/forecast")
async def get_public_weather_forecast(
    city: str = Query(None),
    lat: float = Query(None, ge=-90, le=90),
    lon: float = Query(None, ge=-180, le=180)
):
    """Get weather forecast (public) - accepts either city or lat/lon"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.ENVIRONMENT_SERVICE_URL}/api/v1/weather/forecast"
            params = {}
            if city:
                params["city"] = city
            if lat is not None and lon is not None:
                params["lat"] = lat
                params["lon"] = lon
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching forecast: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# ============================================
# Export Endpoints
# ============================================

@router.get("/export/air-quality")
async def export_air_quality(
    format: str = Query("json", regex="^(json|csv|geojson)$")
):
    """
    Export air quality data in multiple formats
    
    Formats: json, csv, geojson
    """
    # TODO: Implement export service integration
    return {
        "message": "Export feature coming soon",
        "format": format,
        "service": "export-service"
    }


@router.get("/catalog")
async def get_data_catalog():
    """Get OpenData catalog"""
    # TODO: Implement catalog service integration
    return {
        "datasets": [
            {
                "id": "air-quality",
                "title": "Air Quality Data",
                "category": "environment",
                "formats": ["json", "csv", "geojson"],
                "api_endpoint": "/api/open-data/air-quality"
            },
            {
                "id": "weather",
                "title": "Weather Data",
                "category": "environment",
                "formats": ["json"],
                "api_endpoint": "/api/open-data/weather/current"
            }
        ]
    }


# ============================================
# Centers & Resources Endpoints
# ============================================

@router.get("/centers")
async def get_public_centers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get public rescue centers"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.RESOURCE_SERVICE_URL}/api/v1/centers/"
            params = {"skip": skip, "limit": limit}
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Error fetching centers: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/centers/nearby")
async def get_nearby_centers(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10.0, ge=0.1, le=100)
):
    """Get rescue centers near a location"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.RESOURCE_SERVICE_URL}/api/v1/centers/nearby"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "radius_km": radius_km
            }
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Error fetching nearby centers: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

