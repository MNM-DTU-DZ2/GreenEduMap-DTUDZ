from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.green_resource import GreenResource
from app.schemas.green_resource import GreenResourceCreate, GreenResourceUpdate, GreenResourceResponse

router = APIRouter(prefix="/green-resources", tags=["Green Resources"])

@router.post("/", response_model=GreenResourceResponse, status_code=201)
async def create_green_resource(resource: GreenResourceCreate, db: AsyncSession = Depends(get_db)):
    """Tạo tài nguyên xanh mới"""
    db_resource = GreenResource(**resource.model_dump())
    db.add(db_resource)
    await db.commit()
    await db.refresh(db_resource)
    return db_resource

@router.get("/", response_model=List[GreenResourceResponse])
async def list_green_resources(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Lấy danh sách tài nguyên xanh"""
    result = await db.execute(select(GreenResource).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{resource_id}", response_model=GreenResourceResponse)
async def get_green_resource(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lấy thông tin chi tiết tài nguyên xanh"""
    result = await db.execute(select(GreenResource).where(GreenResource.id == resource_id))
    resource = result.scalar_one_or_none()
    if resource is None:
        raise HTTPException(status_code=404, detail="Green resource not found")
    return resource

@router.put("/{resource_id}", response_model=GreenResourceResponse)
async def update_green_resource(resource_id: UUID, resource_update: GreenResourceUpdate, db: AsyncSession = Depends(get_db)):
    """Cập nhật thông tin tài nguyên xanh"""
    result = await db.execute(select(GreenResource).where(GreenResource.id == resource_id))
    db_resource = result.scalar_one_or_none()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Green resource not found")
    
    update_data = resource_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_resource, key, value)

    await db.commit()
    await db.refresh(db_resource)
    return db_resource

@router.delete("/{resource_id}", status_code=204)
async def delete_green_resource(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    """Xóa tài nguyên xanh"""
    result = await db.execute(select(GreenResource).where(GreenResource.id == resource_id))
    db_resource = result.scalar_one_or_none()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Green resource not found")
    
    await db.delete(db_resource)
    await db.commit()
    return None

@router.get("/zone/{zone_id}", response_model=List[GreenResourceResponse])
async def list_resources_by_zone(zone_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lấy danh sách tài nguyên xanh theo khu vực"""
    result = await db.execute(select(GreenResource).where(GreenResource.zone_id == zone_id))
    return result.scalars().all()
