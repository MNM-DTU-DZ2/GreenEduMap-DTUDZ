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
    except Exception as e:
        logger.error(f"Error fetching air quality: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# ============================================
# Weather Endpoints
# ============================================

@router.get("/weather/current")
async def get_public_current_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
):
    """Get current weather (public)"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.ENVIRONMENT_SERVICE_URL}/api/v1/weather/current"
            params = {"lat": lat, "lon": lon, "fetch_new": True}
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/weather/forecast")
async def get_public_weather_forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
):
    """Get weather forecast (public)"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.ENVIRONMENT_SERVICE_URL}/api/v1/weather/forecast"
            params = {"lat": lat, "lon": lon}
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
