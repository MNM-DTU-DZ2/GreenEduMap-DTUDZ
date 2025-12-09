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

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from geoalchemy2 import Geography
from app.core.database import Base

class School(Base):
    """Trường học - Schools with green metrics"""
    __tablename__ = "schools"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    
    # Location (PostGIS Geography)
    location = Column(Geography('POINT', srid=4326), nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    district = Column(String, nullable=True)
    
    # School Information
    type = Column(String, nullable=False)  # elementary, middle, high, university
    total_students = Column(Integer, default=0)
    total_teachers = Column(Integer, default=0)
    
    # Green Metrics
    green_score = Column(Float, default=0.0)
    total_trees = Column(Integer, default=0)
    green_area = Column(Float, default=0.0)
    
    # Contact
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    
    # OpenData
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String, nullable=True)
    ngsi_ld_uri = Column(String, nullable=True)
    
    facilities = Column(JSONB, nullable=True)
    meta_data = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    courses = relationship("GreenCourse", back_populates="school", cascade="all, delete-orphan")
    activities = relationship("GreenActivity", back_populates="school", cascade="all, delete-orphan")

