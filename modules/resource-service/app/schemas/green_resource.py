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
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class GreenResourceBase(BaseModel):
    name: str
    type: str  # trees, solar_panels, wind_turbines, recycling_bins, composters
    quantity: int = Field(..., ge=0)
    available_quantity: int = Field(..., ge=0)
    unit: str
    status: str = "active"
    expiry_date: Optional[datetime] = None
    is_public: bool = True
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class GreenResourceCreate(GreenResourceBase):
    zone_id: UUID

class GreenResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    available_quantity: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = None
    status: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class GreenResourceResponse(GreenResourceBase):
    id: UUID
    zone_id: Optional[UUID] = None  # Allow None for resources without zone
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
