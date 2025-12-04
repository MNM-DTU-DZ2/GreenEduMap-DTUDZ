from fastapi import APIRouter, Query, HTTPException
import httpx
import logging
from typing import Optional

from ..config import settings

router = APIRouter(prefix="/api/open-data", tags=["OpenData - Resources"])
logger = logging.getLogger(__name__)

@router.get("/green-zones")
async def get_public_green_zones(
    skip: int = 0, 
    limit: int = 100
):
    """Get public green zones"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.RESOURCE_SERVICE_URL}/api/v1/green-zones"
            response = await client.get(url, params={"skip": skip, "limit": limit}, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error proxying to resource service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.get("/green-zones/nearby")
async def get_nearby_green_zones(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: float = Query(10.0, ge=0.1, le=100.0)
):
    """Find green zones nearby"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.RESOURCE_SERVICE_URL}/api/v1/green-zones/nearby"
            params = {"latitude": lat, "longitude": lon, "radius_km": radius}
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching nearby green zones: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.get("/green-resources")
async def get_public_green_resources(
    skip: int = 0, 
    limit: int = 100
):
    """Get public green resources"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.RESOURCE_SERVICE_URL}/api/v1/green-resources"
            response = await client.get(url, params={"skip": skip, "limit": limit}, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error proxying to resource service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
