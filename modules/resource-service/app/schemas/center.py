from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime
from uuid import UUID

class RescueCenterBase(BaseModel):
    name: str
    code: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    total_capacity: Optional[int] = None
    current_occupancy: int = 0
    manager_name: Optional[str] = None
    phone: Optional[str] = None
    is_public: bool = True
    data_uri: Optional[str] = None
    facilities: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None

class RescueCenterCreate(RescueCenterBase):
    pass

class RescueCenterUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    total_capacity: Optional[int] = None
    current_occupancy: Optional[int] = None
    manager_name: Optional[str] = None
    phone: Optional[str] = None
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    facilities: Optional[Dict[str, Any]] = None
    meta_data: Optional[Dict[str, Any]] = None

class RescueCenterResponse(RescueCenterBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
