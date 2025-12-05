"""
Environment Service proxy routes
Air Quality + Weather endpoints
"""
from fastapi import APIRouter, Request, Response, Query, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Environment"])

ENVIRONMENT_SERVICE_URL = "http://environment-service:8007"

logger = logging.getLogger(__name__)


# ========== Air Quality Endpoints ==========

@router.get("/air-quality")
async def list_air_quality(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List air quality data (Proxy to environment-service)
    """
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            url = f"{ENVIRONMENT_SERVICE_URL}/api/v1/air-quality/"
            params = dict(request.query_params)
            response = await client.get(url, params=params)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to environment service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/air-quality/{item_id}")
async def get_air_quality(item_id: str):
    """Get specific air quality reading"""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            url = f"{ENVIRONMENT_SERVICE_URL}/api/v1/air-quality/{item_id}/"
            response = await client.get(url)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to environment service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/air-quality/latest")
async def get_latest_air_quality(request: Request):
    """Get latest air quality readings"""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            url = f"{ENVIRONMENT_SERVICE_URL}/api/v1/air-quality/latest/"
            params = dict(request.query_params)
            response = await client.get(url, params=params)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to environment service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# ========== Weather Endpoints ==========

@router.get("/weather")
async def list_weather(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    List weather data (Proxy to environment-service)
    """
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            url = f"{ENVIRONMENT_SERVICE_URL}/api/v1/weather/"
            params = dict(request.query_params)
            response = await client.get(url, params=params)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to environment service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/weather/current")
async def get_current_weather(request: Request):
    """Get current weather"""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            url = f"{ENVIRONMENT_SERVICE_URL}/api/v1/weather/current/"
            params = dict(request.query_params)
            response = await client.get(url, params=params)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to environment service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/weather/{item_id}")
async def get_weather(item_id: str):
    """Get specific weather observation"""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            url = f"{ENVIRONMENT_SERVICE_URL}/api/v1/weather/{item_id}/"
            response = await client.get(url)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to environment service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

