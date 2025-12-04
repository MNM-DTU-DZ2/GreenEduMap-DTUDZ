from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class GreenCourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str  # environment, energy, sustainability, recycling, conservation
    duration_hours: Optional[int] = Field(None, ge=0)
    max_students: int = Field(default=30, ge=1)
    instructor_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    syllabus: Optional[Dict[str, Any]] = None
    learning_outcomes: Optional[Dict[str, Any]] = None
    status: str = 'draft'
    is_public: bool = True

class GreenCourseCreate(GreenCourseBase):
    school_id: UUID

class GreenCourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration_hours: Optional[int] = Field(None, ge=0)
    max_students: Optional[int] = Field(None, ge=1)
    instructor_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    syllabus: Optional[Dict[str, Any]] = None
    learning_outcomes: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    is_public: Optional[bool] = None

class GreenCourseResponse(GreenCourseBase):
    id: UUID
    school_id: UUID
    enrolled_students: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
