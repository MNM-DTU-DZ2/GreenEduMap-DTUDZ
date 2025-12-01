"""
Schools and Green Courses API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.school import School, GreenCourse
from app.schemas.school import (
    SchoolCreate, SchoolUpdate, SchoolResponse,
    GreenCourseCreate, GreenCourseUpdate, GreenCourseResponse,
    BulkImportResponse
)
from app.services.green_score import GreenScoreService

router = APIRouter(prefix="/api/v1", tags=["Education"])


# ========================================
# Schools Endpoints
# ========================================

@router.post("/schools/{school_id}/calculate-score", response_model=SchoolResponse)
async def calculate_school_score(school_id: UUID, db: AsyncSession = Depends(get_db)):
    """Force recalculate Green Score for a school"""
    await GreenScoreService.calculate_score(school_id, db)
    
    # Fetch updated school
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
        
    return school


@router.post("/schools/bulk-import", response_model=BulkImportResponse, status_code=201)
async def bulk_import_schools(schools: List[SchoolCreate], db: AsyncSession = Depends(get_db)):
    """Bulk import schools from JSON list"""
    response = BulkImportResponse(total=len(schools), success=0, failed=0)
    
    for school_data in schools:
        try:
            # Check if code exists
            existing = await db.execute(select(School).where(School.code == school_data.code))
            if existing.scalar_one_or_none():
                response.failed += 1
                response.errors.append(f"School code {school_data.code} already exists")
                continue
                
            # Create Point geometry
            location = func.ST_GeogFromText(f"SRID=4326;POINT({school_data.longitude} {school_data.latitude})")
            
            db_school = School(
                name=school_data.name,
                code=school_data.code,
                location=location,
                address=school_data.address,
                type=school_data.type,
                green_score=school_data.green_score,
                is_public=school_data.is_public,
                data_uri=school_data.data_uri,
                facilities=school_data.facilities,
                meta_data=school_data.meta_data
            )
            db.add(db_school)
            await db.flush() # Get ID without committing yet
            
            # Calculate score
            await GreenScoreService.calculate_score(db_school.id, db)
            
            response.success += 1
            response.ids.append(db_school.id)
            
        except Exception as e:
            response.failed += 1
            response.errors.append(f"Error importing {school_data.name}: {str(e)}")
            
    await db.commit()
    return response


@router.post("/schools", response_model=SchoolResponse, status_code=201)
async def create_school(school: SchoolCreate, db: AsyncSession = Depends(get_db)):
    """Create a new school"""
    # Create Point geometry from lat/lon
    location = func.ST_GeogFromText(f"SRID=4326;POINT({school.longitude} {school.latitude})")
    
    db_school = School(
        name=school.name,
        code=school.code,
        location=location,
        address=school.address,
        type=school.type,
        green_score=school.green_score, # Initial score
        is_public=school.is_public,
        data_uri=school.data_uri,
        facilities=school.facilities,
        meta_data=school.meta_data
    )
    db.add(db_school)
    await db.commit()
    await db.refresh(db_school)
    
    # Calculate real score based on facilities
    await GreenScoreService.calculate_score(db_school.id, db)
    await db.refresh(db_school)
    
    return db_school


@router.get("/schools", response_model=List[SchoolResponse])
async def list_schools(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    type: str = Query(None),
    min_green_score: float = Query(None, ge=0, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List schools with optional filters"""
    query = select(School)
    
    if type:
        query = query.where(School.type == type)
    
    if min_green_score is not None:
        query = query.where(School.green_score >= min_green_score)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    schools = result.scalars().all()
    return schools


@router.get("/schools/nearby", response_model=List[SchoolResponse])
async def get_nearby_schools(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10.0, ge=0.1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Find schools near a location"""
    # Create point from coordinates
    point = func.ST_GeogFromText(f"SRID=4326;POINT({longitude} {latitude})")
    
    # Query schools within radius
    query = select(School).where(
        func.ST_DWithin(School.location, point, radius_km * 1000)  # meters
    ).order_by(
        func.ST_Distance(School.location, point)
    )
    
    result = await db.execute(query)
    schools = result.scalars().all()
    return schools


@router.get("/schools/rankings", response_model=List[SchoolResponse])
async def get_school_rankings(
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get schools ranked by green score"""
    query = select(School).order_by(School.green_score.desc()).limit(limit)
    result = await db.execute(query)
    schools = result.scalars().all()
    return schools


@router.get("/schools/{school_id}", response_model=SchoolResponse)
async def get_school(school_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific school by ID"""
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    return school


@router.put("/schools/{school_id}", response_model=SchoolResponse)
async def update_school(
    school_id: UUID,
    school_update: SchoolUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a school"""
    result = await db.execute(select(School).where(School.id == school_id))
    db_school = result.scalar_one_or_none()
    
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Update fields
    update_data = school_update.model_dump(exclude_unset=True)
    
    # Handle location update if lat/lon provided
    if "latitude" in update_data and "longitude" in update_data:
        db_school.location = func.ST_GeogFromText(
            f"SRID=4326;POINT({update_data['longitude']} {update_data['latitude']})"
        )
        del update_data["latitude"]
        del update_data["longitude"]
    
    for field, value in update_data.items():
        setattr(db_school, field, value)
    
    await db.commit()
    
    # Recalculate score
    await GreenScoreService.calculate_score(school_id, db)
    await db.refresh(db_school)
    
    return db_school


@router.delete("/schools/{school_id}", status_code=204)
async def delete_school(school_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a school"""
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    await db.execute(delete(School).where(School.id == school_id))
    await db.commit()
    return None


# ========================================
# Green Courses Endpoints
# ========================================

@router.post("/green-courses", response_model=GreenCourseResponse, status_code=201)
async def create_green_course(course: GreenCourseCreate, db: AsyncSession = Depends(get_db)):
    """Create a new green course"""
    # Verify school exists
    result = await db.execute(select(School).where(School.id == course.school_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="School not found")
    
    db_course = GreenCourse(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    
    # Recalculate school score
    await GreenScoreService.calculate_score(course.school_id, db)
    
    return db_course


@router.get("/green-courses", response_model=List[GreenCourseResponse])
async def list_green_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List green courses with optional filters"""
    query = select(GreenCourse)
    
    if category:
        query = query.where(GreenCourse.category == category)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    courses = result.scalars().all()
    return courses


@router.get("/green-courses/{course_id}", response_model=GreenCourseResponse)
async def get_green_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific course by ID"""
    result = await db.execute(select(GreenCourse).where(GreenCourse.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course


@router.get("/green-courses/by-school/{school_id}", response_model=List[GreenCourseResponse])
async def get_courses_by_school(school_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get all courses for a specific school"""
    query = select(GreenCourse).where(GreenCourse.school_id == school_id)
    result = await db.execute(query)
    courses = result.scalars().all()
    return courses


@router.put("/green-courses/{course_id}", response_model=GreenCourseResponse)
async def update_green_course(
    course_id: UUID,
    course_update: GreenCourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a green course"""
    result = await db.execute(select(GreenCourse).where(GreenCourse.id == course_id))
    db_course = result.scalar_one_or_none()
    
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    await db.commit()
    await db.refresh(db_course)
    
    # Recalculate school score
    await GreenScoreService.calculate_score(db_course.school_id, db)
    
    return db_course


@router.delete("/green-courses/{course_id}", status_code=204)
async def delete_green_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a green course"""
    result = await db.execute(select(GreenCourse).where(GreenCourse.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    school_id = course.school_id
    await db.execute(delete(GreenCourse).where(GreenCourse.id == course_id))
    await db.commit()
    
    # Recalculate school score
    await GreenScoreService.calculate_score(school_id, db)
    
    return None
