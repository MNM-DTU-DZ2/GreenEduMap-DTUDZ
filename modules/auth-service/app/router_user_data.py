#!/usr/bin/env python3
"""
GreenEduMap-DTUDZ - User Data API Router
API endpoints for user favorites, contributions, activities, settings
"""

from typing import Annotated, List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from geoalchemy2.functions import ST_GeogFromText

from app.core.database import get_db
from app.dependencies import get_current_active_user, require_role
from app.models import User
from app.models_user_data import UserFavorite, UserContribution, UserActivity, UserSettings
from app.schemas_user_data import (
    UserFavoriteCreate, UserFavoriteUpdate, UserFavoriteResponse, UserFavoriteListResponse,
    UserContributionCreate, UserContributionUpdate, UserContributionResponse, UserContributionListResponse,
    UserContributionReview,
    UserActivityCreate, UserActivityResponse, UserActivityListResponse,
    UserSettingsCreate, UserSettingsUpdate, UserSettingsResponse,
)


router = APIRouter(prefix="/api/v1/user-data", tags=["User Data"])


# ================================
# User Favorites Endpoints
# ================================

@router.get("/favorites", response_model=UserFavoriteListResponse)
async def list_favorites(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    target_type: Optional[str] = None,
):
    """Get current user's favorites list."""
    query = select(UserFavorite).where(UserFavorite.user_id == current_user.id)
    
    if target_type:
        query = query.where(UserFavorite.target_type == target_type)
    
    # Count total
    count_query = select(func.count()).select_from(
        query.subquery()
    )
    total = (await db.execute(count_query)).scalar()
    
    # Get items
    query = query.order_by(UserFavorite.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return UserFavoriteListResponse(total=total, items=items)


@router.post("/favorites", response_model=UserFavoriteResponse, status_code=status.HTTP_201_CREATED)
async def create_favorite(
    favorite: UserFavoriteCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Add a new favorite location."""
    # Check if already favorited
    existing = await db.execute(
        select(UserFavorite).where(
            and_(
                UserFavorite.user_id == current_user.id,
                UserFavorite.target_type == favorite.target_type,
                UserFavorite.target_id == favorite.target_id
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already in favorites"
        )
    
    db_favorite = UserFavorite(
        user_id=current_user.id,
        target_type=favorite.target_type,
        target_id=favorite.target_id,
        note=favorite.note,
        is_public=favorite.is_public,
    )
    db.add(db_favorite)
    await db.commit()
    await db.refresh(db_favorite)
    
    return db_favorite


@router.delete("/favorites/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    favorite_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Remove a favorite."""
    result = await db.execute(
        select(UserFavorite).where(
            and_(
                UserFavorite.id == favorite_id,
                UserFavorite.user_id == current_user.id
            )
        )
    )
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    await db.delete(favorite)
    await db.commit()


# ================================
# User Contributions Endpoints
# ================================

@router.get("/contributions", response_model=UserContributionListResponse)
async def list_contributions(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    type: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
):
    """Get current user's contributions."""
    query = select(UserContribution).where(UserContribution.user_id == current_user.id)
    
    if type:
        query = query.where(UserContribution.type == type)
    if status_filter:
        query = query.where(UserContribution.status == status_filter)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()
    
    # Items
    query = query.order_by(UserContribution.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return UserContributionListResponse(total=total, items=items)


@router.get("/contributions/public", response_model=UserContributionListResponse)
async def list_public_contributions(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    type: Optional[str] = None,
):
    """Get all public approved contributions."""
    query = select(UserContribution).where(
        and_(
            UserContribution.is_public == True,
            UserContribution.status == "approved"
        )
    )
    
    if type:
        query = query.where(UserContribution.type == type)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()
    
    # Items
    query = query.order_by(UserContribution.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return UserContributionListResponse(total=total, items=items)


@router.post("/contributions", response_model=UserContributionResponse, status_code=status.HTTP_201_CREATED)
async def create_contribution(
    contribution: UserContributionCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Create a new contribution (AQI report, green spot, issue, feedback)."""
    db_contribution = UserContribution(
        user_id=current_user.id,
        type=contribution.type,
        title=contribution.title,
        description=contribution.description,
        latitude=contribution.latitude,
        longitude=contribution.longitude,
        address=contribution.address,
        is_public=contribution.is_public,
        data=contribution.data,
        status="pending",
    )
    
    # Set location if lat/lon provided
    if contribution.latitude and contribution.longitude:
        db_contribution.location = f"SRID=4326;POINT({contribution.longitude} {contribution.latitude})"
    
    db.add(db_contribution)
    await db.commit()
    await db.refresh(db_contribution)
    
    return db_contribution


@router.get("/contributions/{contribution_id}", response_model=UserContributionResponse)
async def get_contribution(
    contribution_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Get a specific contribution."""
    result = await db.execute(
        select(UserContribution).where(UserContribution.id == contribution_id)
    )
    contribution = result.scalar_one_or_none()
    
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribution not found"
        )
    
    # Check permission
    if contribution.user_id != current_user.id and not contribution.is_public:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this contribution"
            )
    
    return contribution


@router.patch("/contributions/{contribution_id}", response_model=UserContributionResponse)
async def update_contribution(
    contribution_id: UUID,
    update_data: UserContributionUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Update a contribution."""
    result = await db.execute(
        select(UserContribution).where(
            and_(
                UserContribution.id == contribution_id,
                UserContribution.user_id == current_user.id
            )
        )
    )
    contribution = result.scalar_one_or_none()
    
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribution not found"
        )
    
    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(contribution, key, value)
    
    contribution.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(contribution)
    
    return contribution


@router.patch("/contributions/{contribution_id}/review", response_model=UserContributionResponse)
async def review_contribution(
    contribution_id: UUID,
    review: UserContributionReview,
    current_user: Annotated[User, Depends(require_role("admin"))],
    db: AsyncSession = Depends(get_db),
):
    """Review (approve/reject) a contribution. Admin only."""
    result = await db.execute(
        select(UserContribution).where(UserContribution.id == contribution_id)
    )
    contribution = result.scalar_one_or_none()
    
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribution not found"
        )
    
    contribution.status = review.status
    contribution.reviewed_by = current_user.id
    contribution.reviewed_at = datetime.utcnow()
    contribution.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(contribution)
    
    return contribution


@router.delete("/contributions/{contribution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contribution(
    contribution_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Delete a contribution."""
    result = await db.execute(
        select(UserContribution).where(UserContribution.id == contribution_id)
    )
    contribution = result.scalar_one_or_none()
    
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribution not found"
        )
    
    # Check permission
    if contribution.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this contribution"
        )
    
    await db.delete(contribution)
    await db.commit()


# ================================
# User Activities Endpoints
# ================================

@router.get("/activities", response_model=UserActivityListResponse)
async def list_activities(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    action: Optional[str] = None,
):
    """Get current user's activity log."""
    query = select(UserActivity).where(UserActivity.user_id == current_user.id)
    
    if action:
        query = query.where(UserActivity.action == action)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()
    
    # Items
    query = query.order_by(UserActivity.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return UserActivityListResponse(total=total, items=items)


@router.get("/activities/public/{user_id}", response_model=UserActivityListResponse)
async def list_user_public_activities(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
):
    """Get a user's public activities."""
    query = select(UserActivity).where(
        and_(
            UserActivity.user_id == user_id,
            UserActivity.is_public == True
        )
    )
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()
    
    # Items
    query = query.order_by(UserActivity.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return UserActivityListResponse(total=total, items=items)


@router.post("/activities", response_model=UserActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity: UserActivityCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Log a new activity."""
    db_activity = UserActivity(
        user_id=current_user.id,
        action=activity.action,
        target_type=activity.target_type,
        target_id=activity.target_id,
        description=activity.description,
        extra_data=activity.extra_data,
        is_public=activity.is_public,
    )
    
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    
    return db_activity


# ================================
# User Settings Endpoints
# ================================

@router.get("/settings", response_model=UserSettingsResponse)
async def get_settings(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Get current user's settings."""
    result = await db.execute(
        select(UserSettings).where(UserSettings.user_id == current_user.id)
    )
    settings = result.scalar_one_or_none()
    
    if not settings:
        # Create default settings
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
    
    return settings


@router.put("/settings", response_model=UserSettingsResponse)
async def update_settings(
    settings_data: UserSettingsUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db),
):
    """Update current user's settings."""
    result = await db.execute(
        select(UserSettings).where(UserSettings.user_id == current_user.id)
    )
    settings = result.scalar_one_or_none()
    
    if not settings:
        # Create with provided data
        settings = UserSettings(
            user_id=current_user.id,
            **settings_data.model_dump(exclude_unset=True)
        )
        db.add(settings)
    else:
        # Update existing
        update_dict = settings_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(settings, key, value)
        settings.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(settings)
    
    return settings
