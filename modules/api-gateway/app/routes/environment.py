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


@router.get("/weather/forecast")
async def get_weather_forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
):
    """Get weather forecast from environment service"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{ENVIRONMENT_SERVICE_URL}/api/v1/weather/forecast"
            params = {"lat": lat, "lon": lon}
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



