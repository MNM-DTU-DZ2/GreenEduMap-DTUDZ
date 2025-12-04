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


@router.get("/")
async def list_air_quality(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_session)
):
    """List all air quality measurements"""
    try:
        from sqlalchemy import text
        
        # Use raw SQL to extract lat/lon from Geography
        query = """
            SELECT 
                id,
                ST_Y(location::geometry) as latitude,
                ST_X(location::geometry) as longitude,
                aqi, pm25, pm10, co, no2, o3, so2,
                source, station_name, station_id,
                measurement_date, created_at
            FROM air_quality
            WHERE is_public = true
            ORDER BY measurement_date DESC
            LIMIT :limit OFFSET :skip
        """
        
        result = await db.execute(text(query), {"limit": limit, "skip": skip})
        rows = result.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": str(row[0]),
                "latitude": float(row[1]) if row[1] else None,
                "longitude": float(row[2]) if row[2] else None,
                "aqi": float(row[3]) if row[3] else None,
                "pm25": float(row[4]) if row[4] else None,
                "pm10": float(row[5]) if row[5] else None,
                "co": float(row[6]) if row[6] else None,
                "no2": float(row[7]) if row[7] else None,
                "o3": float(row[8]) if row[8] else None,
                "so2": float(row[9]) if row[9] else None,
                "source": row[10],
                "station_name": row[11],
                "station_id": row[12],
                "measurement_date": row[13].isoformat() if row[13] else None,
                "created_at": row[14].isoformat() if row[14] else None
            })
        
        return {
            "total": len(data),
            "skip": skip,
            "limit": limit,
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Error fetching air quality: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/latest")
async def get_latest_air_quality(
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_session)
):
    """Get latest air quality measurements"""
    try:
        from sqlalchemy import text
        
        # Get latest measurements from last 24 hours
        since = datetime.utcnow() - timedelta(days=1)
        
        query = """
            SELECT 
                id,
                ST_Y(location::geometry) as latitude,
                ST_X(location::geometry) as longitude,
                aqi, pm25, pm10, co, no2, o3, so2,
                source, station_name, station_id,
                measurement_date, created_at
            FROM air_quality
            WHERE is_public = true
              AND measurement_date >= :since
            ORDER BY measurement_date DESC
            LIMIT :limit
        """
        
        result = await db.execute(text(query), {"since": since, "limit": limit})
        rows = result.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "id": str(row[0]),
                "latitude": float(row[1]) if row[1] else None,
                "longitude": float(row[2]) if row[2] else None,
                "aqi": float(row[3]) if row[3] else None,
                "pm25": float(row[4]) if row[4] else None,
                "pm10": float(row[5]) if row[5] else None,
                "co": float(row[6]) if row[6] else None,
                "no2": float(row[7]) if row[7] else None,
                "o3": float(row[8]) if row[8] else None,
                "so2": float(row[9]) if row[9] else None,
                "source": row[10],
                "station_name": row[11],
                "station_id": row[12],
                "measurement_date": row[13].isoformat() if row[13] else None,
                "created_at": row[14].isoformat() if row[14] else None
            })
        
        return {
            "total": len(data),
            "data": data
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
