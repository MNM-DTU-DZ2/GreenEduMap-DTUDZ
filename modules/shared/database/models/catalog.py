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

"""
Data Catalog model for OpenData platform
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID

from ..base import Base


class DataCatalog(Base):
    """
    Catalog of available datasets for OpenData platform
    """

    __tablename__ = "data_catalog"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Basic info
    title = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=True)
    category = Column(
        String(100), nullable=False
    )  # 'environment'|'rescue'|'education'|'ai'

    # Dataset info
    table_name = Column(String(255), nullable=False)
    api_endpoint = Column(String(500), nullable=False)
    download_url = Column(String(500), nullable=True)

    # Formats available
    download_formats = Column(ARRAY(String), default=["json", "csv"])
    # e.g., ['json', 'csv', 'geojson', 'rdf']

    # Licensing
    license = Column(String(100), default="MIT")
    is_public = Column(Boolean, default=True, nullable=False)

    # Update info
    update_frequency = Column(
        String(50), nullable=True
    )  # 'real-time'|'hourly'|'daily'|'weekly'
    last_updated = Column(DateTime(timezone=True), nullable=True)

    # Usage statistics
    download_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)

    # Schema
    schema_fields = Column(JSONB, nullable=True)
    # Example: [{"name": "aqi", "type": "float", "description": "Air Quality Index"}]

    # Coverage
    spatial_coverage = Column(JSONB, nullable=True)
    # Example: {"type": "Polygon", "coordinates": [...]}

    temporal_coverage = Column(JSONB, nullable=True)
    # Example: {"start": "2024-01-01", "end": "present"}

    # Documentation
    documentation_url = Column(String(500), nullable=True)

    # Tags for search
    tags = Column(ARRAY(String), nullable=True)

    # Metadata
    meta_data = Column(JSONB, nullable=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<DataCatalog(id={self.id}, title={self.title}, category={self.category})>"
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "formats": self.download_formats,
            "license": self.license,
            "api_endpoint": self.api_endpoint,
            "download_url": self.download_url,
            "update_frequency": self.update_frequency,
            "last_updated": (
                self.last_updated.isoformat() if self.last_updated else None
            ),
            "schema": self.schema_fields,
            "spatial_coverage": self.spatial_coverage,
            "temporal_coverage": self.temporal_coverage,
            "documentation": self.documentation_url,
            "tags": self.tags,
            "stats": {"downloads": self.download_count, "views": self.view_count},
        }
