"""
Air Quality model - OpenData compliant
"""

from datetime import datetime
from uuid import uuid4

from geoalchemy2 import Geography
from sqlalchemy import Boolean, Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from ..base import Base


class AirQuality(Base):
    """
    Air Quality measurements from OpenAQ and sensors
    NGSI-LD compliant for Linked Open Data
    """
    __tablename__ = "air_quality"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Geospatial data (PostGIS)
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    # Air quality measurements
    aqi = Column(Numeric(10, 2), nullable=True)  # Air Quality Index
    pm25 = Column(Numeric(10, 2), nullable=True)  # PM2.5 (µg/m³)
    pm10 = Column(Numeric(10, 2), nullable=True)  # PM10 (µg/m³)
    co = Column(Numeric(10, 2), nullable=True)  # Carbon Monoxide (µg/m³)
    no2 = Column(Numeric(10, 2), nullable=True)  # Nitrogen Dioxide (µg/m³)
    o3 = Column(Numeric(10, 2), nullable=True)  # Ozone (µg/m³)
    so2 = Column(Numeric(10, 2), nullable=True)  # Sulfur Dioxide (µg/m³)

    # Data source
    source = Column(String(50), nullable=False)  # 'openaq' | 'sensor' | 'manual'
    station_name = Column(String(255), nullable=True)
    station_id = Column(String(100), nullable=True)

    # OpenData fields
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(
        String(500), nullable=True
    )  # e.g., /api/open-data/air-quality/{id}
    ngsi_ld_uri = Column(
        String(500), nullable=True
    )  # e.g., urn:ngsi-ld:AirQuality:HN-001

    # Temporal data
    measurement_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Extensibility
    meta_data = Column(JSONB, nullable=True)  # Additional metadata

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Indexes
    __table_args__ = (
        # Spatial index is created automatically by PostGIS
        # Additional indexes
        {"comment": "Air quality measurements from OpenAQ and sensors"}
    )

    def __repr__(self):
        return f"<AirQuality(id={self.id}, aqi={self.aqi}, source={self.source})>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": str(self.id),
            "location": (
                {
                    "type": "Point",
                    "coordinates": [self.location.longitude, self.location.latitude],
                }
                if self.location
                else None
            ),
            "aqi": float(self.aqi) if self.aqi else None,
            "pm25": float(self.pm25) if self.pm25 else None,
            "pm10": float(self.pm10) if self.pm10 else None,
            "co": float(self.co) if self.co else None,
            "no2": float(self.no2) if self.no2 else None,
            "o3": float(self.o3) if self.o3 else None,
            "so2": float(self.so2) if self.so2 else None,
            "source": self.source,
            "station_name": self.station_name,
            "measurement_date": (
                self.measurement_date.isoformat() if self.measurement_date else None
            ),
            "metadata": self.meta_data,
        }

    def to_ngsi_ld(self):
        """Convert to NGSI-LD format"""
        return {
            "id": self.ngsi_ld_uri or f"urn:ngsi-ld:AirQuality:{self.id}",
            "type": "AirQuality",
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://greenedumap.vn/context/environment.jsonld",
            ],
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
            "aqi": (
                {
                    "type": "Property",
                    "value": float(self.aqi),
                    "observedAt": self.measurement_date.isoformat(),
                }
                if self.aqi
                else None
            ),
            "pm25": (
                {"type": "Property", "value": float(self.pm25), "unitCode": "µg/m³"}
                if self.pm25
                else None
            ),
            "pm10": (
                {"type": "Property", "value": float(self.pm10), "unitCode": "µg/m³"}
                if self.pm10
                else None
            ),
            "source": {"type": "Property", "value": self.source},
        }
