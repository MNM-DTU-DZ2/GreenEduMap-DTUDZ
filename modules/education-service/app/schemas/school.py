"""Pydantic schemas for Education Service"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


# ========================================
# School Schemas
# ========================================

class SchoolBase(BaseModel):
    name: str
    code: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    type: str  # elementary, middle, high, university
    green_score: float = Field(default=0.0, ge=0.0, le=100.0)
    is_public: bool = True
    data_uri: Optional[str] = None
    facilities: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address: Optional[str] = None
    type: Optional[str] = None
    green_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    facilities: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None


class SchoolResponse(SchoolBase):
    id: UUID
    ngsi_ld_uri: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ========================================
# Green Course Schemas
# ========================================

class GreenCourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str  # environment, energy, sustainability, recycling
    max_students: Optional[int] = None
    duration_weeks: Optional[int] = None
    is_public: bool = True
    syllabus: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None


class GreenCourseCreate(GreenCourseBase):
    school_id: UUID


class GreenCourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    max_students: Optional[int] = None
    duration_weeks: Optional[int] = None
    is_public: Optional[bool] = None
    syllabus: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None


class GreenCourseResponse(GreenCourseBase):
    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BulkImportResponse(BaseModel):
    total: int
    success: int
    failed: int
    errors: List[str] = []
    ids: List[UUID] = []
