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
    
    # created_at = Column(DateTime(timezone=True), nullable=True)
    # updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    resources = relationship("Resource", back_populates="center", cascade="all, delete-orphan")
