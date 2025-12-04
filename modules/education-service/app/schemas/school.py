from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class SchoolBase(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    type: str  # elementary, middle, high, university
    total_students: int = Field(default=0, ge=0)
    total_teachers: int = Field(default=0, ge=0)
    total_trees: int = Field(default=0, ge=0)
    green_area: float = Field(default=0.0, ge=0)
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    is_public: bool = True
    data_uri: Optional[str] = None
    facilities: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    type: Optional[str] = None
    total_students: Optional[int] = Field(None, ge=0)
    total_teachers: Optional[int] = Field(None, ge=0)
    total_trees: Optional[int] = Field(None, ge=0)
    green_area: Optional[float] = Field(None, ge=0)
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    facilities: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None

class SchoolResponse(SchoolBase):
    id: UUID
    green_score: float
    ngsi_ld_uri: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
