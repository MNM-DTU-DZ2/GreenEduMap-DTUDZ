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
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse

router = APIRouter()

@router.post("/", response_model=ResourceResponse, status_code=201)
async def create_resource(resource: ResourceCreate, db: AsyncSession = Depends(get_db)):
    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    await db.commit()
    await db.refresh(db_resource)
    return db_resource

@router.get("/", response_model=List[ResourceResponse])
async def read_resources(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{resource_id}", response_model=ResourceResponse)
async def read_resource(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: UUID, resource_update: ResourceUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    db_resource = result.scalar_one_or_none()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    update_data = resource_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_resource, key, value)

    await db.commit()
    await db.refresh(db_resource)
    return db_resource

@router.delete("/{resource_id}", status_code=204)
async def delete_resource(resource_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    db_resource = result.scalar_one_or_none()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    await db.delete(db_resource)
    await db.commit()
    return None

@router.get("/center/{center_id}", response_model=List[ResourceResponse])
async def read_resources_by_center(center_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resource).where(Resource.center_id == center_id))
    return result.scalars().all()
