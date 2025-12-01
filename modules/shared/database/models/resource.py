"""
Resource and Rescue Center models
"""

from datetime import datetime
from uuid import uuid4

from geoalchemy2 import Geography
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String)

from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from ..base import Base


class RescueCenter(Base):
    """
    Rescue centers managing resources
    """

    __tablename__ = "rescue_centers"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Basic info
    name = Column(String(500), nullable=False)
    code = Column(String(100), unique=True, nullable=False, index=True)

    # Location
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    address = Column(String(1000), nullable=True)

    # Capacity
    total_capacity = Column(Integer, nullable=True)
    current_occupancy = Column(Integer, default=0)

    # Contact
    manager_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)

    # OpenData fields
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String(500), nullable=True)
    ngsi_ld_uri = Column(String(500), nullable=True)

    # Facilities
    facilities = Column(JSONB, nullable=True)

    # Metadata
    meta_data = Column(JSONB, nullable=True)

    # Relationships
    resources = relationship(
        "Resource", back_populates="center", cascade="all, delete-orphan"
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<RescueCenter(id={self.id}, name={self.name})>"


class Resource(Base):
    """
    Resources managed by rescue centers
    """

    __tablename__ = "resources"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Basic info
    name = Column(String(500), nullable=False)
    type = Column(
        String(100), nullable=False
    )  # 'food'|'water'|'medicine'|'shelter'|'supplies'

    # Quantity
    quantity = Column(Integer, nullable=False, default=0)
    available_quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String(50), nullable=False)  # 'kg', 'liters', 'boxes', 'people'

    # Center relationship
    center_id = Column(
        UUID(as_uuid=True), ForeignKey("rescue_centers.id"), nullable=False
    )
    center = relationship("RescueCenter", back_populates="resources")

    # Status
    status = Column(
        String(50), default="available"
    )  # 'available'|'low_stock'|'out_of_stock'
    expiry_date = Column(DateTime(timezone=True), nullable=True)

    # OpenData fields
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String(500), nullable=True)

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
            f"<Resource(id={self.id}, name={self.name}, "
            f"qty={self.available_quantity}/{self.quantity})>"
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "quantity": self.quantity,
            "available_quantity": self.available_quantity,
            "unit": self.unit,
            "status": self.status,
            "center_id": str(self.center_id),
        }
