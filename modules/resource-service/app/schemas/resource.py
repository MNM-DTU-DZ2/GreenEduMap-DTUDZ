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

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class ResourceBase(BaseModel):
    name: str
    type: str
    quantity: int
    available_quantity: int
    unit: str
    status: str = "available"
    expiry_date: Optional[datetime] = None
    is_public: bool = True
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class ResourceCreate(ResourceBase):
    center_id: UUID

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class ResourceResponse(ResourceBase):
    id: UUID
    center_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
