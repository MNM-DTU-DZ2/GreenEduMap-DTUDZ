from fastapi import APIRouter, Query, HTTPException, Request, Response
import httpx
import logging
from typing import List, Optional
from uuid import UUID

from ..config import settings

logger = logging.getLogger(__name__)

# Router for standard API
router = APIRouter(prefix="/api/v1", tags=["Education"])

# Router for OpenData
opendata_router = APIRouter(prefix="/api/open-data", tags=["OpenData - Education"])

# ==================================================================
# Standard API Endpoints (Proxy to Education Service)
# ==================================================================

@router.get("/schools")
async def list_schools(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    type: Optional[str] = None,
    min_green_score: Optional[float] = None
):
    """List schools (Proxy)"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools"
            params = dict(request.query_params)
            response = await client.get(url, params=params, timeout=30.0)
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.get("/schools/nearby")
async def get_nearby_schools(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10.0, ge=0.1, le=100)
):
    """Get nearby schools (Proxy)"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools/nearby"
            params = dict(request.query_params)
            response = await client.get(url, params=params, timeout=30.0)
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.get("/schools/{school_id}")
async def get_school(school_id: UUID):
    """Get school details (Proxy)"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools/{school_id}"
            response = await client.get(url, timeout=30.0)
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.get("/green-courses")
async def list_green_courses(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None
):
    """List green courses (Proxy)"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/green-courses"
            params = dict(request.query_params)
            response = await client.get(url, params=params, timeout=30.0)
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

# ==================================================================
# OpenData Endpoints
# ==================================================================

@opendata_router.get("/schools")
async def get_opendata_schools(
    format: str = Query("json", regex="^(json|geojson)$"),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get Schools OpenData
    
    Supports:
    - json: Standard list of schools
    - geojson: GeoJSON FeatureCollection
    """
    try:
        async with httpx.AsyncClient() as client:
            # If geojson is requested, we might need a specific endpoint in the service
            # For now, let's assume the service handles it or we proxy to standard list
            # TODO: Implement /api/v1/schools/geojson in Education Service
            
            if format == "geojson":
                # Provisional: proxy to a new endpoint we will create
                url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools/geojson"
            else:
                url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools"
                
            response = await client.get(url, params={"limit": limit}, timeout=30.0)
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
