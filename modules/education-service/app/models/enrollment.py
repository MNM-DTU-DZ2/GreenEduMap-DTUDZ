#!/usr/bin/env python3
"""
GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
Copyright (C) 2025 DTU-DZ2 Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from app.core.database import Base

class Enrollment(Base):
    """Đăng ký khóa học - Course enrollments"""
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("green_courses.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)  # Optional: link to users table if exists
    
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=True)
    student_phone = Column(String, nullable=True)
    
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String, default='enrolled')  # enrolled, completed, dropped
    
    completion_date = Column(DateTime(timezone=True), nullable=True)
    grade = Column(String, nullable=True)
    certificate_url = Column(String, nullable=True)
    
    # Relationships
    course = relationship("GreenCourse", back_populates="enrollments")
