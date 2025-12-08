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
Weather API routes
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin, ST_MakePoint
from datetime import datetime, timedelta
import logging

# Proper imports - shared package is installed
try:
    from shared.database.base import get_session
    from shared.database.models.weather import Weather
except ImportError:
    # Fallback for local development
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from shared.database.base import get_session
    from shared.database.models.weather import Weather

from ..clients import openweather_client

router = APIRouter(prefix="/api/v1/weather", tags=["Weather"])
logger = logging.getLogger(__name__)


@router.get("/")
async def list_weather(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_session)
):
    """List all weather observations"""
    try:
        from sqlalchemy import text
        
        query = """
            SELECT 
                id,
                ST_Y(location::geometry) as latitude,
                ST_X(location::geometry) as longitude,
                city_name, temperature, feels_like, humidity, pressure,
                wind_speed, wind_direction, clouds, visibility,
                weather_main, weather_description,
                source, observation_time, created_at
            FROM weather
            WHERE is_public = true
            ORDER BY observation_time DESC
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
                "city_name": row[3],
                "temperature": float(row[4]) if row[4] else None,
                "feels_like": float(row[5]) if row[5] else None,
                "humidity": int(row[6]) if row[6] else None,
                "pressure": int(row[7]) if row[7] else None,
                "wind_speed": float(row[8]) if row[8] else None,
                "wind_direction": int(row[9]) if row[9] else None,
                "clouds": int(row[10]) if row[10] else None,
                "visibility": int(row[11]) if row[11] else None,
                "weather_main": row[12],
                "weather_description": row[13],
                "source": row[14],
                "observation_time": row[15].isoformat() if row[15] else None,
                "created_at": row[16].isoformat() if row[16] else None
            })
        
        return {
            "total": len(data),
            "skip": skip,
            "limit": limit,
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/current")
async def get_current_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    fetch_new: bool = Query(False),
    db: AsyncSession = Depends(get_session)
):
    """
    Get current weather for a location
    
    Args:
        lat: Latitude
        lon: Longitude
        fetch_new: Fetch fresh data from OpenWeather API
    """
    try:
        if fetch_new:
            # Fetch from OpenWeather API
            weather_data = await openweather_client.get_current_weather(lat, lon)
            
            if weather_data:
                # Save to database
                weather = Weather(
                    location=f"POINT({weather_data['longitude']} {weather_data['latitude']})",
                    city_name=weather_data.get("city_name"),
                    temperature=weather_data.get("temperature"),
                    feels_like=weather_data.get("feels_like"),
                    humidity=weather_data.get("humidity"),
                    pressure=weather_data.get("pressure"),
                    wind_speed=weather_data.get("wind_speed"),
                    wind_direction=weather_data.get("wind_direction"),
                    clouds=weather_data.get("clouds"),
                    visibility=weather_data.get("visibility"),
                    weather_main=weather_data.get("weather_main"),
                    weather_description=weather_data.get("weather_description"),
                    weather_icon=weather_data.get("weather_icon"),
                    rain_1h=weather_data.get("rain_1h"),
                    observation_time=weather_data["observation_time"],
                    sunrise=weather_data.get("sunrise"),
                    sunset=weather_data.get("sunset"),
                    source="openweather",
                    is_public=True
                )
                db.add(weather)
                await db.commit()
                
                # Return data directly without db.refresh() to avoid Geography parsing issues
                return {
                    "id": str(weather.id),
                    "location": {
                        "type": "Point",
                        "coordinates": [weather_data["longitude"], weather_data["latitude"]]
                    },
                    "city_name": weather_data.get("city_name"),
                    "temperature": weather_data.get("temperature"),
                    "feels_like": weather_data.get("feels_like"),
                    "humidity": weather_data.get("humidity"),
                    "pressure": weather_data.get("pressure"),
                    "wind": {
                        "speed": weather_data.get("wind_speed"),
                        "direction": weather_data.get("wind_direction")
                    },
                    "weather": {
                        "main": weather_data.get("weather_main"),
                        "description": weather_data.get("weather_description"),
                        "icon": weather_data.get("weather_icon")
                    },
                    "observation_time": weather_data["observation_time"].isoformat(),
                    "source": "openweather"
                }
        
        # Get from database (recent data)
        since = datetime.utcnow() - timedelta(hours=1)
        radius_meters = 50000  # 50km
        
        # Create point and cast to Geography for ST_DWithin
        point_wkt = f"SRID=4326;POINT({lon} {lat})"
        
        stmt = (
            select(Weather)
            .where(func.ST_DWithin(
                Weather.location,
                func.ST_GeogFromText(point_wkt),
                radius_meters
            ))
            .where(Weather.observation_time >= since)
            .where(Weather.is_public == True)
            .order_by(Weather.observation_time.desc())
            .limit(1)
        )
        
        result = await db.execute(stmt)
        weather = result.scalar_one_or_none()
        
        if weather:
            return weather.to_dict()
        else:
            raise HTTPException(
                status_code=404,
                detail="No recent weather data. Try fetch_new=true"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/forecast")
async def get_weather_forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
):
    """
    Get weather forecast from OpenWeather API
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        5-day forecast with 3-hour intervals
    """
    try:
        forecast_data = await openweather_client.get_forecast(lat, lon)
        
        if not forecast_data:
            raise HTTPException(
                status_code=503,
                detail="Weather forecast service unavailable"
            )
        
        return forecast_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching forecast: {e}\"")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/location")
async def get_weather_by_location(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: int = Query(50, ge=1, le=200),
    hours: int = Query(24, ge=1, le=168),
    db: AsyncSession = Depends(get_session)
):
    """
    Get weather observations near a location
    
    Args:
        lat: Latitude
        lon: Longitude
        radius: Search radius in kilometers
        hours: Hours of history to retrieve
    """
    try:
        since = datetime.utcnow() - timedelta(hours=hours)
        radius_meters = radius * 1000
        point = ST_MakePoint(lon, lat)
        
        stmt = (
            select(Weather)
            .where(ST_DWithin(Weather.location, point, radius_meters))
            .where(Weather.observation_time >= since)
            .where(Weather.is_public == True)
            .order_by(Weather.observation_time.desc())
        )
        
        result = await db.execute(stmt)
        observations = result.scalars().all()
        
        return {
            "location": {"lat": lat, "lon": lon},
            "radius_km": radius,
            "total": len(observations),
            "data": [w.to_dict() for w in observations]
        }
        
    except Exception as e:
        logger.error(f"Error in location search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
