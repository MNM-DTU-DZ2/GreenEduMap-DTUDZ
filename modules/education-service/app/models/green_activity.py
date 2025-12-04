from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from geoalchemy2 import Geography
from app.core.database import Base

class GreenActivity(Base):
    """Hoạt động xanh - Environmental activities"""
    __tablename__ = "green_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    activity_type = Column(String, nullable=False)  # planting, recycling, cleanup, workshop, campaign
    
    # Activity Details
    activity_date = Column(DateTime(timezone=True), nullable=False)
    duration_hours = Column(Float, nullable=True)
    participants_count = Column(Integer, default=0)
    
    # Impact Metrics
    trees_planted = Column(Integer, default=0)
    waste_collected_kg = Column(Float, default=0)
    energy_saved_kwh = Column(Float, default=0)
    
    # Scoring
    impact_points = Column(Integer, default=0)  # Calculated points for green score
    
    # Location (optional - if activity at specific location)
    location = Column(Geography('POINT', srid=4326), nullable=True)
    
    # Media
    photos = Column(JSONB, nullable=True)  # Array of photo URLs
    
    status = Column(String, default='planned')  # planned, ongoing, completed, cancelled
    is_public = Column(Boolean, default=True, nullable=False)
   
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    school = relationship("School", back_populates="activities")
