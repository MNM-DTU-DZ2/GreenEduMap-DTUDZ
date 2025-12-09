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

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from geoalchemy2 import Geography
from app.core.database import Base
import uuid

class RescueCenter(Base):
    __tablename__ = "rescue_centers"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    
    # Geospatial location (Point) - Using GEOGRAPHY as per SQL
    location = Column(Geography('POINT', srid=4326, spatial_index=True), nullable=False)
    address = Column(String, nullable=True)
    
    total_capacity = Column(Integer, nullable=True)
    current_occupancy = Column(Integer, default=0)
    
    manager_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String, nullable=True)
    ngsi_ld_uri = Column(String, nullable=True)
    
    facilities = Column(JSONB, nullable=True)
    meta_data = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    # resources = relationship("Resource", back_populates="center", cascade="all, delete-orphan")
    
    @property
    def latitude(self) -> float:
        """Extract latitude from location Geography field"""
        if self.location is None:
            return None
        from geoalchemy2.shape import to_shape
        point = to_shape(self.location)
        return point.y
    
    @property
    def longitude(self) -> float:
        """Extract longitude from location Geography field"""
        if self.location is None:
            return None
        from geoalchemy2.shape import to_shape
        point = to_shape(self.location)
        return point.x

