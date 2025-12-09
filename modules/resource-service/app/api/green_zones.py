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

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.green_zone import GreenZone
from app.schemas.green_zone import GreenZoneCreate, GreenZoneUpdate, GreenZoneResponse

router = APIRouter(prefix="/green-zones", tags=["Green Zones"])

@router.post("/", response_model=GreenZoneResponse, status_code=201)
async def create_green_zone(zone: GreenZoneCreate, db: AsyncSession = Depends(get_db)):
    """Tạo khu vực xanh mới"""
    from shapely.geometry import Point
    from geoalchemy2.shape import from_shape
    
    # Create Shapely Point (longitude, latitude)
    point = Point(zone.longitude, zone.latitude)
    # Convert to WKB for Geography column
    location_wkb = from_shape(point, srid=4326)
    
    db_zone = GreenZone(
        name=zone.name,
        code=zone.code,
        location=location_wkb,
        address=zone.address,
        zone_type=zone.zone_type,
        area_sqm=zone.area_sqm,
        tree_count=zone.tree_count,
        vegetation_coverage=zone.vegetation_coverage,
        maintained_by=zone.maintained_by,
        phone=zone.phone,
        is_public=zone.is_public,
        data_uri=zone.data_uri,
        facilities=zone.facilities,
        meta_data=zone.meta_data
    )
    db.add(db_zone)
    await db.commit()
    await db.refresh(db_zone)
    return db_zone

@router.get("/", response_model=List[GreenZoneResponse])
async def list_green_zones(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Lấy danh sách các khu vực xanh với latitude/longitude từ location Geography"""
    from sqlalchemy import text
    
    # Extract latitude/longitude from location Geography column
    base_sql = """
        SELECT id, name, code, address, zone_type, area_sqm, tree_count,
               vegetation_coverage, maintained_by, phone, is_public,
               data_uri, ngsi_ld_uri, facilities, meta_data,
               created_at, updated_at,
               ST_Y(location::geometry) as latitude,
               ST_X(location::geometry) as longitude
        FROM green_zones
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :skip
    """
    
    result = await db.execute(text(base_sql), {"limit": limit, "skip": skip})
    
    # Map rows to dict
    zones = []
    for row in result:
        zone_dict = {
            "id": row.id,
            "name": row.name,
            "code": row.code,
            "address": row.address,
            "zone_type": row.zone_type,
            "area_sqm": row.area_sqm,
            "tree_count": row.tree_count or 0,
            "vegetation_coverage": float(row.vegetation_coverage) if row.vegetation_coverage else None,
            "maintained_by": row.maintained_by,
            "phone": row.phone,
            "is_public": row.is_public if row.is_public is not None else True,
            "data_uri": row.data_uri,
            "facilities": row.facilities,
            "meta_data": row.meta_data,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "latitude": float(row.latitude) if row.latitude else None,
            "longitude": float(row.longitude) if row.longitude else None,
        }
        zones.append(zone_dict)
    
    return zones

@router.get("/nearby")
async def find_nearby_zones(
    lat: float = Query(..., ge=-90, le=90), 
    lon: float = Query(..., ge=-180, le=180), 
    radius_km: float = Query(default=10.0, ge=0.1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Tìm các khu vực xanh gần vị trí (geospatial search)"""
    from sqlalchemy import text
    
    # Use raw SQL to avoid Geography serialization issues
    query = """
        SELECT id, name, code, address, zone_type, area_sqm, tree_count,
               vegetation_coverage, maintained_by, phone, is_public,
               data_uri, ngsi_ld_uri, facilities, meta_data,
               created_at, updated_at,
               ST_Y(location::geometry) as latitude,
               ST_X(location::geometry) as longitude,
               ST_Distance(location, ST_GeogFromText(:point)) as distance_m
        FROM green_zones
        WHERE ST_DWithin(location, ST_GeogFromText(:point), :radius_m)
        ORDER BY distance_m ASC
    """
    
    point_wkt = f"SRID=4326;POINT({lon} {lat})"
    result = await db.execute(text(query), {
        "point": point_wkt, 
        "radius_m": radius_km * 1000
    })
    
    zones = []
    for row in result:
        zone_dict = {
            "id": row.id,
            "name": row.name,
            "code": row.code,
            "address": row.address,
            "zone_type": row.zone_type,
            "area_sqm": row.area_sqm,
            "tree_count": row.tree_count or 0,
            "vegetation_coverage": float(row.vegetation_coverage) if row.vegetation_coverage else None,
            "maintained_by": row.maintained_by,
            "phone": row.phone,
            "is_public": row.is_public if row.is_public is not None else True,
            "data_uri": row.data_uri,
            "facilities": row.facilities,
            "meta_data": row.meta_data,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "latitude": float(row.latitude) if row.latitude else None,
            "longitude": float(row.longitude) if row.longitude else None,
            "distance_meters": float(row.distance_m) if row.distance_m else None,
        }
        zones.append(zone_dict)
    
    return zones

@router.get("/{zone_id}", response_model=GreenZoneResponse)
async def get_green_zone(zone_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lấy thông tin chi tiết khu vực xanh"""
    result = await db.execute(select(GreenZone).where(GreenZone.id == zone_id))
    zone = result.scalar_one_or_none()
    if zone is None:
        raise HTTPException(status_code=404, detail="Green zone not found")
    return zone

@router.put("/{zone_id}", response_model=GreenZoneResponse)
async def update_green_zone(zone_id: UUID, zone_update: GreenZoneUpdate, db: AsyncSession = Depends(get_db)):
    """Cập nhật thông tin khu vực xanh"""
    result = await db.execute(select(GreenZone).where(GreenZone.id == zone_id))
    db_zone = result.scalar_one_or_none()
    if db_zone is None:
        raise HTTPException(status_code=404, detail="Green zone not found")
    
    update_data = zone_update.model_dump(exclude_unset=True)
    
    # Handle location update if lat/lon provided
    if "latitude" in update_data and "longitude" in update_data:
        from shapely.geometry import Point
        from geoalchemy2.shape import from_shape
        
        point = Point(update_data['longitude'], update_data['latitude'])
        update_data["location"] = from_shape(point, srid=4326)
        del update_data["latitude"]
        del update_data["longitude"]
    elif "latitude" in update_data or "longitude" in update_data:
        raise HTTPException(status_code=400, detail="Both latitude and longitude must be provided to update location")

    for key, value in update_data.items():
        setattr(db_zone, key, value)

    await db.commit()
    await db.refresh(db_zone)
    return db_zone

@router.delete("/{zone_id}", status_code=204)
async def delete_green_zone(zone_id: UUID, db: AsyncSession = Depends(get_db)):
    """Xóa khu vực xanh"""
    result = await db.execute(select(GreenZone).where(GreenZone.id == zone_id))
    db_zone = result.scalar_one_or_none()
    if db_zone is None:
        raise HTTPException(status_code=404, detail="Green zone not found")
    
    await db.delete(db_zone)
    await db.commit()
    return None
