from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from app.core.database import Base

class Review(Base):
    """
    Review model for school ratings and comments
    """
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False)
    
    # User info (simplified for now, pending full Auth integration)
    user_id = Column(UUID(as_uuid=True), nullable=True) # Can be null for anonymous or if auth not fully ready
    user_name = Column(String, nullable=False)
    
    rating = Column(Integer, nullable=False) # 1-5
    comment = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    school = relationship("School", back_populates="reviews")
