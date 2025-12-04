from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class GreenCourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str  # environment, energy, sustainability, recycling, climate, biodiversity
    duration_weeks: Optional[int] = Field(None, ge=0)
    max_students: Optional[int] = Field(None, ge=1)
    syllabus: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None
    is_public: bool = True

class GreenCourseCreate(GreenCourseBase):
    school_id: UUID

class GreenCourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration_weeks: Optional[int] = Field(None, ge=0)
    max_students: Optional[int] = Field(None, ge=1)
    syllabus: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None

class GreenCourseResponse(GreenCourseBase):
    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
