from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class ResourceBase(BaseModel):
    name: str
    type: str
    quantity: int
    available_quantity: int
    unit: str
    status: str = "available"
    expiry_date: Optional[datetime] = None
    is_public: bool = True
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class ResourceCreate(ResourceBase):
    center_id: UUID

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_public: Optional[bool] = None
    data_uri: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class ResourceResponse(ResourceBase):
    id: UUID
    center_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
