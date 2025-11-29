"""User service - CRUD operations."""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models import User
from app.schemas import UserUpdate


class UserService:
    """User service class."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        is_public: Optional[bool] = None
    ) -> List[User]:
        """Get list of users with pagination."""
        query = select(User)
        
        if role:
            query = query.where(User.role == role)
        
        if is_public is not None:
            query = query.where(User.is_public == is_public)
        
        query = query.offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        """Update user information."""
        user = await self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def delete_user(self, user_id: UUID):
        """Soft delete user (set is_active = False)."""
        user = await self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = False
        await self.db.commit()
    
    async def verify_user(self, user_id: UUID):
        """Verify user account."""
        user = await self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_verified = True
        await self.db.commit()
        
        return user
