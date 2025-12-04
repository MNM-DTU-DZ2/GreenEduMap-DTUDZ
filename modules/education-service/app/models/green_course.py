from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from app.core.database import Base

class GreenCourse(Base):
    """Khóa học xanh - Green Skills courses"""
    __tablename__ = "green_courses"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # environment, energy, sustainability, recycling, climate, biodiversity
    
    # Course Details
    max_students = Column(Integer, nullable=True)
    duration_weeks = Column(Integer, nullable=True)
    
    # Content
    syllabus = Column(JSONB, nullable=True)  # Course outline
    meta_data = Column(JSONB, nullable=True)  # Additional metadata
    
    # Status
    is_public = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    school = relationship("School", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
