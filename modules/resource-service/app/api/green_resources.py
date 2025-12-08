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

@router.get("/")
async def list_green_resources(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Lấy danh sách tài nguyên xanh (cho phép zone_id = None)"""
    # Bỏ response_model để bypass Pydantic validation (vì zone_id có thể None)
    result = await db.execute(select(GreenResource).offset(skip).limit(limit))
    resources = result.scalars().all()
    
    # Convert to dict để handle None zone_id
    resource_list = []
    for resource in resources:
        resource_dict = {
            "id": str(resource.id),
            "name": resource.name,
            "type": resource.type,
            "quantity": resource.quantity or 0,
            "available_quantity": resource.available_quantity or 0,
            "unit": resource.unit,
            "status": resource.status or "active",
            "expiry_date": resource.expiry_date.isoformat() if resource.expiry_date else None,
            "is_public": resource.is_public if resource.is_public is not None else True,
            "data_uri": resource.data_uri,
            "meta_data": resource.meta_data,
            "zone_id": str(resource.zone_id) if resource.zone_id else None,  # Convert UUID to string or None
            "created_at": resource.created_at.isoformat() if resource.created_at else None,
            "updated_at": resource.updated_at.isoformat() if resource.updated_at else None,
        }
        resource_list.append(resource_dict)
    
    return resource_list

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
