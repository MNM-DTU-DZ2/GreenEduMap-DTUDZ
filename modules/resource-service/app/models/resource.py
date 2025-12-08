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

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from app.core.database import Base
import uuid

class Resource(Base):
    __tablename__ = "resources"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)
    unit = Column(String, nullable=False)
    
    center_id = Column(UUID(as_uuid=True), ForeignKey("rescue_centers.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(String, default='available')
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String, nullable=True)
    meta_data = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    center = relationship("RescueCenter", back_populates="resources")
