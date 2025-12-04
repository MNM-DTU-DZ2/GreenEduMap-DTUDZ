"""
NGSI-LD Entities API
Serves entities in NGSI-LD format
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.services.entity_transformer import EntityTransformer

router = APIRouter(prefix="/entities", tags=["NGSI-LD Entities"])


async def load_air_quality_data(db: AsyncSession, limit: int = 100):
    """Load air quality data with geography extraction"""
    query = """
        SELECT 
            id,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            aqi, pm25, pm10, co, no2, o3, so2,
            station_name, station_id, source, measurement_date,
            created_at
        FROM air_quality
        ORDER BY measurement_date DESC
        LIMIT :limit
    """
    result = await db.execute(text(query), {"limit": limit})
    rows = result.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'id': str(row[0]),
            'latitude': float(row[1]) if row[1] else 0,
            'longitude': float(row[2]) if row[2] else 0,
            'aqi': float(row[3]) if row[3] else None,
            'pm25': float(row[4]) if row[4] else None,
            'pm10': float(row[5]) if row[5] else None,
            'co': float(row[6]) if row[6] else None,
            'no2': float(row[7]) if row[7] else None,
            'o3': float(row[8]) if row[8] else None,
            'so2': float(row[9]) if row[9] else None,
            'station_name': row[10],
            'station_id': row[11],
            'source': row[12],
            'measurement_date': row[13],
            'created_at': row[14]
        })
    
    return data


async def load_schools_data(db: AsyncSession, limit: int = 100):
    """Load schools data with geography extraction"""
    query = """
        SELECT 
            id, name, code, address, city, district,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            green_score, total_students, total_teachers, type,
            created_at, updated_at
        FROM schools
        ORDER BY created_at DESC
        LIMIT :limit
    """
    result = await db.execute(text(query), {"limit": limit})
    rows = result.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'id': str(row[0]),
            'name': row[1],
            'code': row[2],
            'address': row[3],
            'city': row[4],
            'district': row[5],
            'latitude': float(row[6]) if row[6] else 0,
            'longitude': float(row[7]) if row[7] else 0,
            'green_score': float(row[8]) if row[8] else None,
            'total_students': int(row[9]) if row[9] else None,
            'total_teachers': int(row[10]) if row[10] else None,
            'type': row[11],
            'created_at': row[12],
            'updated_at': row[13]
        })
    
    return data


async def load_green_zones_data(db: AsyncSession, limit: int = 100):
    """Load green zones data"""
    query = """
        SELECT 
            id, name, zone_type, description,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            area_sqm, amenities, opening_hours, entry_fee, rating,
            created_at, updated_at
        FROM green_zones
        ORDER BY created_at DESC
        LIMIT :limit
    """
    result = await db.execute(text(query), {"limit": limit})
    rows = result.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'id': str(row[0]),
            'name': row[1],
            'zone_type': row[2],
            'description': row[3],
            'latitude': float(row[4]) if row[4] else 0,
            'longitude': float(row[5]) if row[5] else 0,
            'area_sqm': float(row[6]) if row[6] else None,
            'amenities': row[7],
            'opening_hours': row[8],
            'entry_fee': float(row[9]) if row[9] else None,
            'rating': float(row[10]) if row[10] else None,
            'created_at': row[11],
            'updated_at': row[12]
        })
    
    return data


async def load_green_courses_data(db: AsyncSession, limit: int = 100):
    """Load green courses data"""
    query = """
        SELECT 
            id, school_id, title, description, category,
            duration_weeks, start_date, end_date,
            instructor_name, max_participants, is_active,
            created_at, updated_at
        FROM green_courses
        WHERE is_active = true
        ORDER BY created_at DESC
        LIMIT :limit
    """
    result = await db.execute(text(query), {"limit": limit})
    rows = result.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'id': str(row[0]),
            'school_id': str(row[1]) if row[1] else None,
            'title': row[2],
            'description': row[3],
            'category': row[4],
            'duration_weeks': int(row[5]) if row[5] else None,
            'start_date': row[6],
            'end_date': row[7],
            'instructor_name': row[8],
            'max_participants': int(row[9]) if row[9] else None,
            'is_active': row[10],
            'created_at': row[11],
            'updated_at': row[12]
        })
    
    return data


@router.get("")
async def list_entities(
    type: Optional[str] = Query(None, description="Entity type filter"),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    List NGSI-LD entities
    
    Args:
        type: Filter by entity type (School, AirQualityObserved, GreenZone, GreenCourse)
        limit: Maximum number of entities to return
        
    Returns:
        List of NGSI-LD entities
    """
    entities = []
    
    if type is None or type == "AirQualityObserved":
        air_quality = await load_air_quality_data(db, limit if type else min(limit, 50))
        for item in air_quality:
            entity = EntityTransformer.db_to_ngsi_ld("air_quality", item)
            entities.append(entity)
    
    if type is None or type == "School":
        schools = await load_schools_data(db, limit if type else min(limit, 50))
        for item in schools:
            entity = EntityTransformer.db_to_ngsi_ld("school", item)
            entities.append(entity)
    
    if type is None or type == "GreenZone":
        zones = await load_green_zones_data(db, limit if type else min(limit, 50))
        for item in zones:
            entity = EntityTransformer.db_to_ngsi_ld("green_zone", item)
            entities.append(entity)
    
    if type is None or type == "GreenCourse":
        courses = await load_green_courses_data(db, limit if type else min(limit, 50))
        for item in courses:
            entity = EntityTransformer.db_to_ngsi_ld("green_course", item)
            entities.append(entity)
    
    return entities[:limit]


@router.get("/{entity_id}")
async def get_entity(
    entity_id: str,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get single NGSI-LD entity by ID
    
    Args:
        entity_id: Entity UUID
        
    Returns:
        NGSI-LD entity
    """
    # Try each table
    tables = [
        ("air_quality", "air_quality"),
        ("schools", "school"),
        ("green_zones", "green_zone"),
        ("green_courses", "green_course")
    ]
    
    for table_name, entity_type in tables:
        if table_name in ["air_quality", "schools"]:
            query = f"""
                SELECT 
                    id,
                    ST_Y(location::geometry) as latitude,
                    ST_X(location::geometry) as longitude,
                    *
                FROM {table_name}
                WHERE id::text = :entity_id
            """
        else:
            query = f"""
                SELECT 
                    id,
                    ST_Y(location::geometry) as latitude,
                    ST_X(location::geometry) as longitude,
                    *
                FROM {table_name}
                WHERE id::text = :entity_id
            """
        
        result = await db.execute(text(query), {"entity_id": entity_id})
        row = result.fetchone()
        
        if row:
            # Convert to dict (simplified, actual implementation needs proper mapping)
            data = dict(row._mapping)
            entity = EntityTransformer.db_to_ngsi_ld(entity_type, data)
            return entity
    
    raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")

