from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class EnrollmentBase(BaseModel):
    student_name: str
    student_email: Optional[str] = None
    student_phone: Optional[str] = None

class EnrollmentCreate(EnrollmentBase):
    course_id: UUID
    user_id: Optional[UUID] = None

class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None
    completion_date: Optional[datetime] = None
    grade: Optional[str] = None
    certificate_url: Optional[str] = None

class EnrollmentResponse(EnrollmentBase):
    id: UUID
    course_id: UUID
    user_id: Optional[UUID] = None
    enrollment_date: datetime
    status: str
    completion_date: Optional[datetime] = None
    grade: Optional[str] = None
    certificate_url: Optional[str] = None

    class Config:
        from_attributes = True
