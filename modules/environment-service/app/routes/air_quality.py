"""
Air Quality API routes
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from geoalchemy2.functions import ST_DWithin, ST_MakePoint
from typing import List, Optional
from datetime import datetime, timedelta
import logging

# Proper imports - shared package is installed
try:
    from shared.database.base import get_session
    from shared.database.models.air_quality import AirQuality
except ImportError:
    # Fallback for local development
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from shared.database.base import get_session
    from shared.database.models.air_quality import AirQuality

from ..clients import openaq_client

router = APIRouter(prefix="/api/v1/air-quality", tags=["Air Quality"])
logger = logging.getLogger(__name__)


@router.get("/latest")
async def get_latest_air_quality(
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_session)
):
    """Get latest air quality measurements"""
    try:
        # Get latest measurements from last 24 hours
        since = datetime.utcnow() - timedelta(days=1)
        
        stmt = (
            select(AirQuality)
            .where(AirQuality.measurement_date >= since)
            .where(AirQuality.is_public == True)
            .order_by(AirQuality.measurement_date.desc())
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        measurements = result.scalars().all()
        
        return {
            "total": len(measurements),
            "data": [m.to_dict() for m in measurements]
        }
        
    except Exception as e:
        logger.error(f"Error fetching air quality: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/location")
async def get_air_quality_by_location(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: int = Query(50, ge=1, le=200),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_session)
):
    """
    Get air quality measurements near a location
    
    Args:
        lat: Latitude
        lon: Longitude
        radius: Search radius in kilometers
        limit: Max results to return
    """
    try:
        # Convert radius from km to meters
        radius_meters = radius * 1000
        
        # Create point geometry
        point = ST_MakePoint(lon, lat)
        
        # Query with spatial filter
        stmt = (
            select(AirQuality)
            .where(ST_DWithin(AirQuality.location, point, radius_meters))
            .where(AirQuality.is_public == True)
            .order_by(AirQuality.measurement_date.desc())
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        measurements = result.scalars().all()
        
        return {
            "location": {"lat": lat, "lon": lon},
            "radius_km": radius,
            "total": len(measurements),
            "data": [m.to_dict() for m in measurements]
        }
        
    except Exception as e:
        logger.error(f"Error in location search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history")
async def get_air_quality_history(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    days: int = Query(7, ge=1, le=90),
    radius: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_session)
):
    """
    Get historical air quality data for a location
    
    Args:
        lat: Latitude
        lon: Longitude  
        days: Number of days of history (max 90)
        radius: Search radius in kilometers
    """
    try:
        since = datetime.utcnow() - timedelta(days=days)
        radius_meters = radius * 1000
        point = ST_MakePoint(lon, lat)
        
        stmt = (
            select(AirQuality)
            .where(ST_DWithin(AirQuality.location, point, radius_meters))
            .where(AirQuality.measurement_date >= since)
            .where(AirQuality.is_public == True)
            .order_by(AirQuality.measurement_date.asc())
        )
        
        result = await db.execute(stmt)
        measurements = result.scalars().all()
        
        return {
            "location": {"lat": lat, "lon": lon},
            "period": {"start": since.isoformat(), "end": datetime.utcnow().isoformat()},
            "total": len(measurements),
            "data": [m.to_dict() for m in measurements]
        }
        
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{measurement_id}")
async def get_air_quality_by_id(
    measurement_id: str,
    db: AsyncSession = Depends(get_session)
):
    """Get specific air quality measurement by ID"""
    try:
        stmt = select(AirQuality).where(AirQuality.id == measurement_id)
        result = await db.execute(stmt)
        measurement = result.scalar_one_or_none()
        
        if not measurement:
            raise HTTPException(status_code=404, detail="Measurement not found")
        
        return measurement.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching measurement: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/fetch")
async def fetch_air_quality_data(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_session)
):
    """
    Manually trigger fetching air quality data from OpenAQ
    (Admin endpoint)
    """
    try:
        # Fetch from OpenAQ
        measurements = await openaq_client.get_latest_measurements(lat, lon, radius * 1000)
        
        saved_count = 0
        for raw in measurements:
            parsed = openaq_client.parse_measurement(raw)
            if parsed:
                # Create AirQuality record
                aq = AirQuality(
                    location=f"POINT({parsed['longitude']} {parsed['latitude']})",
                    station_name=parsed.get("station_name"),
                    source=parsed["source"],
                    measurement_date=parsed["measurement_date"],
                    aqi=parsed["measurements"].get("aqi"),
                    pm25=parsed["measurements"].get("pm25"),
                    pm10=parsed["measurements"].get("pm10"),
                    co=parsed["measurements"].get("co"),
                    no2=parsed["measurements"].get("no2"),
                    o3=parsed["measurements"].get("o3"),
                    so2=parsed["measurements"].get("so2"),
                    is_public=True
                )
                db.add(aq)
                saved_count += 1
        
        await db.commit()
        
        return {
            "status": "success",
            "fetched": len(measurements),
            "saved": saved_count
        }
        
    except Exception as e:
        logger.error(f"Error fetching OpenAQ data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
