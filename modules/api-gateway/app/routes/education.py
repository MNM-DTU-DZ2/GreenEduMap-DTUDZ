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

import logging
from typing import Optional
from uuid import UUID

import httpx
from fastapi import APIRouter, HTTPException, Query, Request, Response

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
    min_green_score: Optional[float] = None,
):
    """List schools (Proxy)"""
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools/"  # Added trailing slash
            params = dict(request.query_params)
            response = await client.get(url, params=params, timeout=30.0)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/schools/nearby")
async def get_nearby_schools(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10.0, ge=0.1, le=100),
):
    """Get nearby schools (Proxy)"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools/nearby"
            params = dict(request.query_params)
            response = await client.get(url, params=params, timeout=30.0)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
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
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/green-courses")
async def list_green_courses(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
):
    """List green courses (Proxy)"""
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/courses/"  # Fixed endpoint with trailing slash
            params = dict(request.query_params)
            response = await client.get(url, params=params, timeout=30.0)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# ==================================================================
# OpenData Endpoints
# ==================================================================


@opendata_router.get("/schools")
async def get_opendata_schools(
    format: str = Query("json", regex="^(json|geojson)$"),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Get Schools OpenData

    Supports:
    - json: Standard list of schools
    - geojson: GeoJSON FeatureCollection
    """
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # For now just return json, geojson to be implemented later
            url = f"{settings.EDUCATION_SERVICE_URL}/api/v1/schools/"  # Added trailing slash

            response = await client.get(url, params={"limit": limit}, timeout=30.0)
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type"),
            )
    except Exception as e:
        logger.error(f"Error proxying to education service: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
