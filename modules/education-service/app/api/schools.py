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
from sqlalchemy import select, func, desc, text
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate, SchoolResponse

router = APIRouter(prefix="/schools", tags=["Schools"])

@router.post("/", response_model=SchoolResponse, status_code=201)
async def create_school(school: SchoolCreate, db: AsyncSession = Depends(get_db)):
    """Tạo trường học mới (Geography updated via raw SQL)"""
    
    # Create school without Geography column (ORM doesn't include it)
    db_school = School(
        name=school.name,
        code=school.code,
        latitude=school.latitude,
        longitude=school.longitude,
        address=school.address,
        school_type=school.school_type,
        total_students=school.total_students,
        total_teachers=school.total_teachers,
        total_trees=school.total_trees,
        green_area=school.green_area,
        principal_name=school.principal_name,
        phone=school.phone,
        email=school.email,
        website=school.website,
        is_public=school.is_public,
        data_uri=school.data_uri,
        facilities=school.facilities,
        meta_data=school.meta_data
    )
    db.add(db_school)
    await db.flush()  # Get the ID without committing
    
    # Update location Geography column using raw SQL
    await db.execute(
        text("UPDATE schools SET location = ST_GeogFromText(:geog) WHERE id = :id"),
        {"geog": f"SRID=4326;POINT({school.longitude} {school.latitude})", "id": db_school.id}
    )
    
    await db.commit()
    await db.refresh(db_school)
    return db_school

@router.get("/", response_model=List[SchoolResponse])
async def list_schools(
    skip: int = 0, 
    limit: int = 100,
    school_type: str = Query(None, description="Filter by school type"),
    db: AsyncSession = Depends(get_db)
):
    """Lấy danh sách trường học với latitude/longitude từ location Geography"""
    # Extract latitude/longitude from location Geography column
    base_sql = """
        SELECT id, name, code, address, city, district, type,
               total_students, total_teachers, total_trees, green_area,
               phone, email, website, green_score, is_public,
               data_uri, ngsi_ld_uri, facilities, meta_data,
               created_at, updated_at,
               ST_Y(location::geometry) as latitude,
               ST_X(location::geometry) as longitude
        FROM schools
    """
    
    params = {}
    conditions = []
    
    if school_type:
        conditions.append("type = :school_type")
        params["school_type"] = school_type
    
    if conditions:
        base_sql += " WHERE " + " AND ".join(conditions)
    
    base_sql += " ORDER BY green_score DESC LIMIT :limit OFFSET :skip"
    params["limit"] = limit
    params["skip"] = skip
    
    result = await db.execute(text(base_sql), params)
    
    # Map rows to dict (bypass Pydantic validation for now)
    schools = []
    for row in result:
        school_dict = {
            "id": row.id,
            "name": row.name,
            "code": row.code,
            "address": row.address,
            "city": row.city,
            "district": row.district,
            "type": row.type,
            "total_students": row.total_students or 0,
            "total_teachers": row.total_teachers or 0,
            "total_trees": row.total_trees or 0,
            "green_area": float(row.green_area) if row.green_area else 0.0,
            "phone": row.phone,
            "email": row.email,
            "website": row.website,
            "green_score": float(row.green_score) if row.green_score else 0.0,
            "is_public": row.is_public if row.is_public is not None else True,
            "data_uri": row.data_uri,
            "ngsi_ld_uri": row.ngsi_ld_uri,
            "facilities": row.facilities,
            "meta_data": row.meta_data,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "latitude": float(row.latitude) if row.latitude else None,
            "longitude": float(row.longitude) if row.longitude else None,
        }
        schools.append(school_dict)
    
    return schools

@router.get("/nearby", response_model=List[SchoolResponse])
async def find_nearby_schools(
    latitude: float = Query(..., ge=-90, le=90), 
    longitude: float = Query(..., ge=-180, le=180), 
    radius_km: float = Query(default=10.0, ge=0.1, le=100),
    school_type: str = Query(None, description="Filter by school type"),
    db: AsyncSession = Depends(get_db)
):
    """Tìm trường học gần vị trí (raw SQL geospatial search)"""
    
    # Build dynamic SQL - extract lat/lon from location Geography column
    base_sql = """
        SELECT id, name, code, 
               ST_Y(location::geometry) as latitude, 
               ST_X(location::geometry) as longitude,
               address, city, district, type as school_type, 
               total_students, total_teachers, total_trees, green_area,
               phone, email, website, green_score, is_public, 
               data_uri, ngsi_ld_uri, facilities, meta_data, created_at, updated_at
        FROM schools
        WHERE ST_DWithin(
            location,
            ST_GeogFromText(:point),
            :radius
        )
    """
    
    params = {
        "point": f"SRID=4326;POINT({longitude} {latitude})", 
        "radius": radius_km * 1000
    }
    
    if school_type:
        base_sql += " AND type = :school_type"
        params["school_type"] = school_type
    
    base_sql += " ORDER BY green_score DESC"
    
    result = await db.execute(text(base_sql), params)
    
    # Map rows to dict
    schools = []
    for row in result:
        school_dict = {
            "id": row.id,
            "name": row.name,
            "code": row.code,
            "latitude": float(row.latitude) if row.latitude else None,
            "longitude": float(row.longitude) if row.longitude else None,
            "address": row.address,
            "city": getattr(row, 'city', None),
            "district": getattr(row, 'district', None),
            "type": row.school_type,
            "total_students": row.total_students or 0,
            "total_teachers": row.total_teachers or 0,
            "total_trees": row.total_trees or 0,
            "green_area": float(row.green_area) if row.green_area else 0.0,
            "phone": row.phone,
            "email": row.email,
            "website": row.website,
            "green_score": float(row.green_score) if row.green_score else 0.0,
            "is_public": row.is_public if row.is_public is not None else True,
            "data_uri": row.data_uri,
            "ngsi_ld_uri": row.ngsi_ld_uri,
            "facilities": row.facilities,
            "meta_data": row.meta_data,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }
        schools.append(school_dict)
    
    return schools


@router.get("/ranking", response_model=List[SchoolResponse])
async def get_school_ranking(
    limit: int = Query(default=10, ge=1, le=100),
    school_type: str = Query(None, description="Filter by school type"),
    db: AsyncSession = Depends(get_db)
):
    """Xếp hạng trường xanh nhất"""
    query = select(School).order_by(desc(School.green_score))
    
    if school_type:
        query = query.where(School.school_type == school_type)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(school_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lấy thông tin chi tiết trường học"""
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.put("/{school_id}", response_model=SchoolResponse)
async def update_school(school_id: UUID, school_update: SchoolUpdate, db: AsyncSession = Depends(get_db)):
    """Cập nhật thông tin trường học"""
    result = await db.execute(select(School).where(School.id == school_id))
    db_school = result.scalar_one_or_none()
    if db_school is None:
        raise HTTPException(status_code=404, detail="School not found")
    
    update_data = school_update.model_dump(exclude_unset=True)
    
    # Update location Geography if lat/lon changed
    if "latitude" in update_data and "longitude" in update_data:
        await db.execute(
            text("UPDATE schools SET location = ST_GeogFromText(:geog) WHERE id = :id"),
            {"geog": f"SRID=4326;POINT({update_data['longitude']} {update_data['latitude']})", "id": school_id}
        )

    for key, value in update_data.items():
        setattr(db_school, key, value)

    await db.commit()
    await db.refresh(db_school)
    return db_school

@router.delete("/{school_id}", status_code=204)
async def delete_school(school_id: UUID, db: AsyncSession = Depends(get_db)):
    """Xóa trường học"""
    result = await db.execute(select(School).where(School.id == school_id))
    db_school = result.scalar_one_or_none()
    if db_school is None:
        raise HTTPException(status_code=404, detail="School not found")
    
    await db.delete(db_school)
    await db.commit()
    return None

@router.get("/{school_id}/stats")
async def get_school_stats(school_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lấy thống kê của trường"""
    from app.models.green_course import GreenCourse
    from app.models.green_activity import GreenActivity
    
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Count courses
    courses_result = await db.execute(
        select(func.count(GreenCourse.id)).where(GreenCourse.school_id == school_id)
    )
    courses_count = courses_result.scalar()
    
    # Count activities
    activities_result = await db.execute(
        select(func.count(GreenActivity.id)).where(GreenActivity.school_id == school_id)
    )
    activities_count = activities_result.scalar()
    
    # Sum impact metrics
    impact_result = await db.execute(
        select(
            func.sum(GreenActivity.trees_planted),
            func.sum(GreenActivity.waste_collected_kg),
            func.sum(GreenActivity.energy_saved_kwh)
        ).where(GreenActivity.school_id == school_id)
    )
    impact = impact_result.first()
    
    return {
        "school_id": school_id,
        "school_name": school.name,
        "green_score": school.green_score,
        "courses_count": courses_count,
        "activities_count": activities_count,
        "total_trees": school.total_trees,
        "total_trees_planted": impact[0] or 0,
        "total_waste_collected_kg": impact[1] or 0,
        "total_energy_saved_kwh": impact[2] or 0
    }
