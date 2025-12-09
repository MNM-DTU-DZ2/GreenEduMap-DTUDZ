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
from typing import Optional
from datetime import datetime
from uuid import UUID

class EnrollmentBase(BaseModel):
    student_name: str
    student_email: Optional[str] = None
    student_phone: Optional[str] = None

class EnrollmentCreate(EnrollmentBase):
    course_id: UUID
    user_id: Optional[UUID] = None

class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None
    completion_date: Optional[datetime] = None
    grade: Optional[str] = None
    certificate_url: Optional[str] = None

class EnrollmentResponse(EnrollmentBase):
    id: UUID
    course_id: UUID
    user_id: Optional[UUID] = None
    enrollment_date: datetime
    status: str
    completion_date: Optional[datetime] = None
    grade: Optional[str] = None
    certificate_url: Optional[str] = None

    class Config:
        from_attributes = True
