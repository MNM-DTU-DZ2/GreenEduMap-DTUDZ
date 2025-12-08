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

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from uuid import UUID

class GreenZoneBase(BaseModel):
    name: str
    code: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    zone_type: Optional[str] = None  # park, forest, garden, green_space
    area_sqm: Optional[int] = Field(None, ge=0)
    tree_count: int = Field(default=0, ge=0)
    vegetation_coverage: Optional[float] = Field(None, ge=0, le=100)
    maintained_by: Optional[str] = None
    phone: Optional[str] = None
    is_public: bool = True
    data_uri: Optional[str] = None
    facilities: Optional[Union[Dict[str, Any], List[str]]] = None  # Accept both dict and list
    meta_data: Optional[Dict[str, Any]] = None

class GreenZoneCreate(GreenZoneBase):
    pass

class GreenZoneUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address: Optional[str] = None
    zone_type: Optional[str] = None
    area_sqm: Optional[int] = Field(None, ge=0)
    tree_count: Optional[int] = Field(None, ge=0)
    vegetation_coverage: Optional[float] = Field(None, ge=0, le=100)
    maintained_by: Optional[str] = None
    phone: Optional[str] = None
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    facilities: Optional[Union[Dict[str, Any], List[str]]] = None  # Accept both dict and list
    meta_data: Optional[Dict[str, Any]] = None

class GreenZoneResponse(GreenZoneBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
