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
    
    # Coordinates (for serialization and queries)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    
    # Note: location Geography column exists in DB but not loaded by ORM to avoid serialization issues
    
    # School Information
    school_type = Column(String, nullable=False)  # elementary, middle, high, university
    total_students = Column(Integer, default=0)
    total_teachers = Column(Integer, default=0)
    
    # Green Metrics
    green_score = Column(Float, default=0.0)
    total_trees = Column(Integer, default=0)
    green_area = Column(Float, default=0.0)
    
    # Management
    principal_name = Column(String, nullable=True)
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

