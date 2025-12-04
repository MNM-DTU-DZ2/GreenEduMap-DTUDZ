from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from app.core.database import Base
import uuid

class GreenResource(Base):
    """Tài nguyên xanh - Green resources (trees, solar panels, etc.)"""
    __tablename__ = "green_resources"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # trees, solar_panels, wind_turbines, recycling_bins
    quantity = Column(Integer, default=0, nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)
    unit = Column(String, nullable=False)  # e.g., pieces, kWh, kg
    
    zone_id = Column(UUID(as_uuid=True), ForeignKey("green_zones.id", ondelete="CASCADE"), nullable=False)
    
    status = Column(String, default='active')
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    is_public = Column(Boolean, default=True, nullable=False)
    data_uri = Column(String, nullable=True)
    meta_data = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    zone = relationship("GreenZone", back_populates="resources")
