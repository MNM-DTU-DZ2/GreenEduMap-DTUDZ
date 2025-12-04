from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from geoalchemy2.elements import WKTElement
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.center import RescueCenter
from app.schemas.center import RescueCenterCreate, RescueCenterUpdate, RescueCenterResponse

router = APIRouter()

@router.post("/", response_model=RescueCenterResponse, status_code=201)
async def create_center(center: RescueCenterCreate, db: AsyncSession = Depends(get_db)):
    # Create Point using Shapely, then convert to Geography
    from shapely.geometry import Point
    from geoalchemy2.shape import from_shape
    
    # Create Shapely Point (longitude, latitude)
    point = Point(center.longitude, center.latitude)
    # Convert to WKB for Geography column
    location_wkb = from_shape(point, srid=4326)
    
    db_center = RescueCenter(
        name=center.name,
        code=center.code,
        location=location_wkb,
        address=center.address,
        total_capacity=center.total_capacity,
        current_occupancy=center.current_occupancy,
        manager_name=center.manager_name,
        phone=center.phone,
        is_public=center.is_public,
        data_uri=center.data_uri,
        facilities=center.facilities,
        meta_data=center.meta_data
    )
    db.add(db_center)
    await db.commit()
    await db.refresh(db_center)
    return db_center

@router.get("/", response_model=List[RescueCenterResponse])
async def read_centers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RescueCenter).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/nearby", response_model=List[RescueCenterResponse])
async def find_nearby_centers(
    latitude: float, 
    longitude: float, 
    radius_km: float = 10.0,
    db: AsyncSession = Depends(get_db)
):
    # Use ST_DWithin for efficient radius search
    # For Geography, ST_DWithin takes distance in meters
    
    stmt = select(RescueCenter).where(
        func.ST_DWithin(
            RescueCenter.location,
            func.ST_GeogFromText(f"SRID=4326;POINT({longitude} {latitude})"),
            radius_km * 1000 # Convert km to meters
        )
    )
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{center_id}", response_model=RescueCenterResponse)
async def read_center(center_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RescueCenter).where(RescueCenter.id == center_id))
    center = result.scalar_one_or_none()
    if center is None:
        raise HTTPException(status_code=404, detail="Rescue center not found")
    return center

@router.put("/{center_id}", response_model=RescueCenterResponse)
async def update_center(center_id: UUID, center_update: RescueCenterUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RescueCenter).where(RescueCenter.id == center_id))
    db_center = result.scalar_one_or_none()
    if db_center is None:
        raise HTTPException(status_code=404, detail="Rescue center not found")
    
    update_data = center_update.model_dump(exclude_unset=True)
    
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
        setattr(db_center, key, value)

    await db.commit()
    await db.refresh(db_center)
    return db_center

@router.delete("/{center_id}", status_code=204)
async def delete_center(center_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RescueCenter).where(RescueCenter.id == center_id))
    db_center = result.scalar_one_or_none()
    if db_center is None:
        raise HTTPException(status_code=404, detail="Rescue center not found")
    
    await db.delete(db_center)
    await db.commit()
    return None
