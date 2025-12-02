from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class ReviewBase(BaseModel):
    user_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: UUID
    school_id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
