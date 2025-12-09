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

class GreenCourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str  # environment, energy, sustainability, recycling, climate, biodiversity
    duration_weeks: Optional[int] = Field(None, ge=0)
    max_students: Optional[int] = Field(None, ge=1)
    syllabus: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None
    is_public: bool = True

class GreenCourseCreate(GreenCourseBase):
    school_id: UUID

class GreenCourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration_weeks: Optional[int] = Field(None, ge=0)
    max_students: Optional[int] = Field(None, ge=1)
    syllabus: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None

class GreenCourseResponse(GreenCourseBase):
    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
