from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from geoalchemy2 import Geography
from app.core.database import Base

class School(Base):
    """
    School model for green education tracking
    Supports spatial queries for location-based searches
    """
    __tablename__ = "schools"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    
    # Geospatial location (Point) - Using GEOGRAPHY for lat/lon queries
    location = Column(Geography('POINT', srid=4326, spatial_index=True), nullable=False)
    address = Column(String, nullable=True)
    
    # School classification
    type = Column(String, nullable=False)  # elementary, middle, high, university
    
    # Green score (0-100)
    green_score = Column(Numeric(5, 2), default=0.0, nullable=False)
    
    # OpenData fields
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String, nullable=True)
    ngsi_ld_uri = Column(String, nullable=True)
    
    # Extensibility
    facilities = Column(JSONB, nullable=True)  # solar panels, gardens, recycling, etc.
    meta_data = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    green_courses = relationship("GreenCourse", back_populates="school", cascade="all, delete-orphan")
    
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


class GreenCourse(Base):
    """
    Green/Environmental courses offered by schools
    Tracks sustainability education programs
    """
    __tablename__ = "green_courses"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)  # environment, energy, sustainability, recycling, etc.
    
    max_students = Column(Integer, nullable=True)
    duration_weeks = Column(Integer, nullable=True)
    
    # OpenData fields
    is_public = Column(Boolean, default=True, nullable=False)
    
    # Course details
    syllabus = Column(JSONB, nullable=True)  # Detailed course structure
    meta_data = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    school = relationship("School", back_populates="green_courses")
