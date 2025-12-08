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
from typing import List, Optional
from uuid import UUID
from app.core.database import get_db
from app.models.green_course import GreenCourse
from app.schemas.green_course import GreenCourseCreate, GreenCourseUpdate, GreenCourseResponse

router = APIRouter(prefix="/courses", tags=["Green Courses"])

@router.get("/", response_model=List[GreenCourseResponse])
async def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    school_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all green courses with optional filters"""
    query = select(GreenCourse)
    
    # Apply filters
    if category:
        query = query.filter(GreenCourse.category == category)
    if school_id:
        query = query.filter(GreenCourse.school_id == school_id)
    
    # Only show public courses by default
    query = query.filter(GreenCourse.is_public == True)
    
    # Pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    courses = result.scalars().all()
    
    return courses


@router.get("/{course_id}", response_model=GreenCourseResponse)
async def get_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific green course by ID"""
    result = await db.execute(
        select(GreenCourse).filter(GreenCourse.id == course_id)
    )
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course


@router.post("/", response_model=GreenCourseResponse, status_code=201)
async def create_course(
    course: GreenCourseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new green course"""
    # Verify school exists
    from app.models.school import School
    result = await db.execute(
        select(School).filter(School.id == course.school_id)
    )
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Create course
    db_course = GreenCourse(
        school_id=course.school_id,
        title=course.title,
        description=course.description,
        category=course.category,
        duration_weeks=course.duration_weeks,
        max_students=course.max_students,
        syllabus=course.syllabus,
        meta_data=course.meta_data,
        is_public=course.is_public
    )
    
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    
    return db_course


@router.put("/{course_id}", response_model=GreenCourseResponse)
async def update_course(
    course_id: UUID,
    course_update: GreenCourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a green course"""
    result = await db.execute(
        select(GreenCourse).filter(GreenCourse.id == course_id)
    )
    db_course = result.scalar_one_or_none()
    
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Update fields
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    await db.commit()
    await db.refresh(db_course)
    
    return db_course


@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a green course"""
    result = await db.execute(
        select(GreenCourse).filter(GreenCourse.id == course_id)
    )
    db_course = result.scalar_one_or_none()
    
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    await db.delete(db_course)
    await db.commit()
    
    return None


@router.get("/categories/list")
async def list_categories():
    """Get list of available course categories"""
    return {
        "categories": [
            {"value": "environment", "label": "Environment"},
            {"value": "energy", "label": "Renewable Energy"},
            {"value": "sustainability", "label": "Sustainability"},
            {"value": "recycling", "label": "Recycling & Waste Management"},
            {"value": "climate", "label": "Climate Change"},
            {"value": "biodiversity", "label": "Biodiversity"}
        ]
    }


@router.get("/stats/summary", response_model=dict)
async def get_courses_stats(
    db: AsyncSession = Depends(get_db)
):
    """Get statistics about green courses"""
    # Total courses
    total_result = await db.execute(
        select(func.count(GreenCourse.id))
    )
    total_courses = total_result.scalar()
    
    # By category
    category_result = await db.execute(
        select(
            GreenCourse.category,
            func.count(GreenCourse.id).label('count')
        ).group_by(GreenCourse.category)
    )
    by_category = {row.category: row.count for row in category_result}
    
    return {
        "total_courses": total_courses,
        "by_category": by_category
    }

