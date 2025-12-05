from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class GreenResourceBase(BaseModel):
    name: str
    type: str  # trees, solar_panels, wind_turbines, recycling_bins, composters
    quantity: int = Field(..., ge=0)
    available_quantity: int = Field(..., ge=0)
    unit: str
    status: str = "active"
    expiry_date: Optional[datetime] = None
    is_public: bool = True
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class GreenResourceCreate(GreenResourceBase):
    zone_id: UUID

class GreenResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    available_quantity: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = None
    status: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class GreenResourceResponse(GreenResourceBase):
    id: UUID
    zone_id: Optional[UUID] = None  # Allow None for resources without zone
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
