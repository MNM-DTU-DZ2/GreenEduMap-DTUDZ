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
