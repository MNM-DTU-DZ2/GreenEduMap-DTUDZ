"""
School model - OpenData compliant
"""

from datetime import datetime
from uuid import uuid4

from geoalchemy2 import Geography
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..base import Base


class School(Base):
    """
    School and educational institution model
    """

    __tablename__ = "schools"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Basic info
    name = Column(String(500), nullable=False)
    code = Column(String(100), unique=True, nullable=False, index=True)

    # Location
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    address = Column(String(1000), nullable=True)
    city = Column(String(255), nullable=True)
    district = Column(String(255), nullable=True)

    # School type
    type = Column(
        String(50), nullable=False
    )  # 'elementary'|'middle'|'high'|'university'

    # Green metrics
    green_score = Column(Numeric(5, 2), nullable=True)  # 0-100
    total_trees = Column(Integer, nullable=True)
    green_area = Column(Numeric(10, 2), nullable=True)  # Square meters

    # Capacity
    total_students = Column(Integer, nullable=True)
    total_teachers = Column(Integer, nullable=True)

    # Contact
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)

    # OpenData fields
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String(500), nullable=True)
    ngsi_ld_uri = Column(String(500), nullable=True)

    # Facilities (JSONB for flexibility)
    facilities = Column(JSONB, nullable=True)
    # Example: {"library": true, "lab": true, "garden": true, "solar_panels": false}

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
            f"<School(id={self.id}, name={self.name}, green_score={self.green_score})>"
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "code": self.code,
            "location": (
                {
                    "type": "Point",
                    "coordinates": [self.location.longitude, self.location.latitude],
                }
                if self.location
                else None
            ),
            "address": self.address,
            "type": self.type,
            "green_score": float(self.green_score) if self.green_score else None,
            "facilities": self.facilities,
            "contact": {
                "phone": self.phone,
                "email": self.email,
                "website": self.website,
            },
        }

    def to_ngsi_ld(self):
        """Convert to NGSI-LD format"""
        return {
            "id": self.ngsi_ld_uri or f"urn:ngsi-ld:School:{self.code}",
            "type": "School",
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://greenedumap.vn/context/education.jsonld",
            ],
            "name": {"type": "Property", "value": self.name},
            "location": (
                {
                    "type": "GeoProperty",
                    "value": {
                        "type": "Point",
                        "coordinates": [
                            self.location.longitude,
                            self.location.latitude,
                        ],
                    },
                }
                if self.location
                else None
            ),
            "greenScore": (
                {"type": "Property", "value": float(self.green_score)}
                if self.green_score
                else None
            ),
            "schoolType": {"type": "Property", "value": self.type},
        }
