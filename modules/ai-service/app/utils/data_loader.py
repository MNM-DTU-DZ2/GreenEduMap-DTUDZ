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
Data Loader - Load data from database for ML models
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


async def load_air_quality_data(
    db: AsyncSession,
    location_id: str = None,
    limit: int = 1000
) -> List[Dict[str, Any]]:
    """
    Load air quality data from database
    
    Args:
        db: Database session
        location_id: Optional location filter
        limit: Max records to load
    
    Returns:
        List of air quality records
    """
    query = """
        SELECT 
            id,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            aqi, pm25, pm10, co, no2, o3, so2,
            station_name,
            measurement_date as measured_at
        FROM air_quality
        WHERE aqi IS NOT NULL
    """
    
    if location_id:
        query += f" AND station_id = '{location_id}'"
    
    query += f" ORDER BY measurement_date DESC LIMIT {limit}"
    
    result = await db.execute(text(query))
    rows = result.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'id': str(row[0]),
            'latitude': float(row[1]) if row[1] else 0,
            'longitude': float(row[2]) if row[2] else 0,
            'aqi': float(row[3]) if row[3] else 0,
            'pm25': float(row[4]) if row[4] else 0,
            'pm10': float(row[5]) if row[5] else 0,
            'co': float(row[6]) if row[6] else 0,
            'no2': float(row[7]) if row[7] else 0,
            'o3': float(row[8]) if row[8] else 0,
            'so2': float(row[9]) if row[9] else 0,
            'station_name': row[10],
            'measured_at': row[11]
        })
    
    logger.info(f"Loaded {len(data)} air quality records")
    return data


async def load_schools_data(
    db: AsyncSession,
    limit: int = 1000
) -> List[Dict[str, Any]]:
    """
    Load schools data from database
    
    Args:
        db: Database session
        limit: Max records to load
    
    Returns:
        List of school records
    """
    query = """
        SELECT 
            id,
            name,
            code,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            green_score,
            total_students,
            total_teachers,
            type
        FROM schools
        WHERE green_score IS NOT NULL
        ORDER BY green_score DESC
        LIMIT :limit
    """
    
    result = await db.execute(text(query), {'limit': limit})
    rows = result.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'id': str(row[0]),
            'name': row[1],
            'code': row[2],
            'latitude': float(row[3]) if row[3] else 0,
            'longitude': float(row[4]) if row[4] else 0,
            'green_score': float(row[5]) if row[5] else 0,
            'total_students': int(row[6]) if row[6] else 0,
            'total_teachers': int(row[7]) if row[7] else 0,
            'type': row[8]
        })
    
    logger.info(f"Loaded {len(data)} school records")
    return data


async def load_combined_data(db: AsyncSession) -> Dict[str, List[Dict[str, Any]]]:
    """
    Load both environment and education data
    
    Args:
        db: Database session
    
    Returns:
        Dict with 'environment' and 'education' keys
    """
    environment_data = await load_air_quality_data(db)
    education_data = await load_schools_data(db)
    
    return {
        'environment': environment_data,
        'education': education_data
    }

