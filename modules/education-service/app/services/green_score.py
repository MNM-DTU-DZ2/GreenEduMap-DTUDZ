"""
Green Score Service
Handles calculation of Green Score for schools based on various metrics.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.school import School, GreenCourse
import logging

logger = logging.getLogger(__name__)

class GreenScoreService:
    @staticmethod
    async def calculate_score(school_id: str, db: AsyncSession) -> float:
        """
        Calculate and update the Green Score for a school.
        
        Formula:
        - Facilities (40%): Solar, gardens, recycling, etc.
        - Courses (30%): Number and quality of green courses
        - Environment (20%): Proximity to clean air (mocked/future)
        - Community (10%): Engagement events (from metadata)
        """
        # Fetch school with courses
        query = select(School).where(School.id == school_id)
        result = await db.execute(query)
        school = result.scalar_one_or_none()
        
        if not school:
            raise ValueError(f"School with ID {school_id} not found")
            
        # Fetch courses
        courses_query = select(GreenCourse).where(GreenCourse.school_id == school_id)
        courses_result = await db.execute(courses_query)
        courses = courses_result.scalars().all()
        
        # 1. Facilities Score (Max 40)
        facilities_score = GreenScoreService._calculate_facilities_score(school.facilities)
        
        # 2. Courses Score (Max 30)
        courses_score = GreenScoreService._calculate_courses_score(courses)
        
        # 3. Environment Score (Max 20) - Mocked for now based on location
        env_score = GreenScoreService._calculate_environment_score(school)
        
        # 4. Community Score (Max 10)
        community_score = GreenScoreService._calculate_community_score(school.meta_data)
        
        # Total Score
        total_score = facilities_score + courses_score + env_score + community_score
        final_score = min(round(total_score, 2), 100.0)
        
        # Update school
        school.green_score = final_score
        await db.commit()
        await db.refresh(school)
        
        logger.info(f"Calculated Green Score for {school.name}: {final_score} "
                    f"(F:{facilities_score}, C:{courses_score}, E:{env_score}, M:{community_score})")
        
        return final_score

    @staticmethod
    def _calculate_facilities_score(facilities: dict) -> float:
        if not facilities:
            return 0.0
            
        score = 0.0
        
        # Infrastructure items
        if facilities.get("solar_panels"): score += 10
        if facilities.get("rain_water_harvest"): score += 10
        if facilities.get("gardens"): score += 10
        if facilities.get("composting"): score += 5
        
        # Recycling bins (1 pt per 10 bins, max 5)
        bins = facilities.get("recycling_bins", 0)
        if isinstance(bins, int):
            score += min(bins / 10, 5)
            
        return min(score, 40.0)

    @staticmethod
    def _calculate_courses_score(courses: list) -> float:
        if not courses:
            return 0.0
            
        score = 0.0
        
        # Quantity (5 pts per course, max 20)
        score += min(len(courses) * 5, 20)
        
        # Quality (Avg duration & size)
        if courses:
            avg_duration = sum(c.duration_weeks or 0 for c in courses) / len(courses)
            if avg_duration > 10:
                score += 5
                
            avg_students = sum(c.max_students or 0 for c in courses) / len(courses)
            if avg_students > 30:
                score += 5
                
        return min(score, 30.0)

    @staticmethod
    def _calculate_environment_score(school) -> float:
        # TODO: Integrate with Environment Service
        # For now, return a baseline score + random variation based on ID hash
        # to simulate different environmental conditions
        import hashlib
        hash_val = int(hashlib.md5(str(school.id).encode()).hexdigest(), 16)
        return 10.0 + (hash_val % 11)  # Returns 10-20

    @staticmethod
    def _calculate_community_score(meta_data: dict) -> float:
        if not meta_data:
            return 0.0
            
        score = 0.0
        events = meta_data.get("events_count", 0)
        if isinstance(events, int):
            score += min(events * 2, 10)
            
        return min(score, 10.0)
