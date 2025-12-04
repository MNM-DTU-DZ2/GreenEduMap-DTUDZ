from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class GreenActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    activity_type: str  # planting, recycling, cleanup, workshop, campaign
    activity_date: datetime
    duration_hours: Optional[float] = Field(None, ge=0)
    participants_count: int = Field(default=0, ge=0)
    trees_planted: int = Field(default=0, ge=0)
    waste_collected_kg: float = Field(default=0, ge=0)
    energy_saved_kwh: float = Field(default=0, ge=0)
    impact_points: int = Field(default=0, ge=0)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    photos: Optional[List[str]] = None
    status: str = 'planned'
    is_public: bool = True

class GreenActivityCreate(GreenActivityBase):
    school_id: UUID

class GreenActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    activity_type: Optional[str] = None
    activity_date: Optional[datetime] = None
    duration_hours: Optional[float] = Field(None, ge=0)
    participants_count: Optional[int] = Field(None, ge=0)
    trees_planted: Optional[int] = Field(None, ge=0)
    waste_collected_kg: Optional[float] = Field(None, ge=0)
    energy_saved_kwh: Optional[float] = Field(None, ge=0)
    impact_points: Optional[int] = Field(None, ge=0)
    status: Optional[str] = None
    is_public: Optional[bool] = None

class GreenActivityResponse(GreenActivityBase):
    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
