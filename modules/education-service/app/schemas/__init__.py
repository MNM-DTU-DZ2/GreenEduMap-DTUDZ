"""Education Service Schemas"""
from app.schemas.school import (
    SchoolBase, SchoolCreate, SchoolUpdate, SchoolResponse,
    GreenCourseBase, GreenCourseCreate, GreenCourseUpdate, GreenCourseResponse
)

__all__ = [
    "SchoolBase", "SchoolCreate", "SchoolUpdate", "SchoolResponse",
    "GreenCourseBase", "GreenCourseCreate", "GreenCourseUpdate", "GreenCourseResponse"
]
