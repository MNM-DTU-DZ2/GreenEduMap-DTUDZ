#!/usr/bin/env python3
"""
GreenEduMap-DTUDZ - User Data Schemas
Pydantic schemas for user favorites, contributions, activities, settings
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, UUID4
from enum import Enum


# ================================
# Enums
# ================================

class TargetType(str, Enum):
    SCHOOL = "school"
    GREEN_ZONE = "green_zone"
    RECYCLING_CENTER = "recycling_center"


class ContributionType(str, Enum):
    AQI_REPORT = "aqi_report"
    GREEN_SPOT = "green_spot"
    ISSUE = "issue"
    FEEDBACK = "feedback"


class ContributionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ActivityAction(str, Enum):
    LOGIN = "login"
    VIEW = "view"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SHARE = "share"
    FAVORITE = "favorite"
    SEARCH = "search"


class PrivacyLevel(str, Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"


# ================================
# User Favorite Schemas
# ================================

class UserFavoriteBase(BaseModel):
    target_type: TargetType
    target_id: UUID4
    note: Optional[str] = None
    is_public: bool = False


class UserFavoriteCreate(UserFavoriteBase):
    pass


class UserFavoriteUpdate(BaseModel):
    note: Optional[str] = None
    is_public: Optional[bool] = None


class UserFavoriteResponse(UserFavoriteBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ================================
# User Contribution Schemas
# ================================

class UserContributionBase(BaseModel):
    type: ContributionType
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address: Optional[str] = None
    is_public: bool = True
    data: Optional[Dict[str, Any]] = None


class UserContributionCreate(UserContributionBase):
    pass


class UserContributionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address: Optional[str] = None
    is_public: Optional[bool] = None
    data: Optional[Dict[str, Any]] = None


class UserContributionReview(BaseModel):
    status: ContributionStatus


class UserContributionResponse(UserContributionBase):
    id: UUID4
    user_id: UUID4
    status: str
    reviewed_by: Optional[UUID4] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ================================
# User Activity Schemas
# ================================

class UserActivityBase(BaseModel):
    action: ActivityAction
    target_type: Optional[str] = None
    target_id: Optional[UUID4] = None
    description: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    is_public: bool = False


class UserActivityCreate(UserActivityBase):
    pass


class UserActivityResponse(UserActivityBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True


# ================================
# User Settings Schemas
# ================================

class UserSettingsBase(BaseModel):
    notification_enabled: bool = True
    email_notifications: bool = True
    push_notifications: bool = True
    language: str = "vi"
    theme: str = "light"
    default_city: str = "TP. Hồ Chí Minh"
    default_latitude: Optional[float] = 10.7769
    default_longitude: Optional[float] = 106.7009
    privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC
    data: Optional[Dict[str, Any]] = None


class UserSettingsCreate(UserSettingsBase):
    pass


class UserSettingsUpdate(BaseModel):
    notification_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    language: Optional[str] = None
    theme: Optional[str] = None
    default_city: Optional[str] = None
    default_latitude: Optional[float] = None
    default_longitude: Optional[float] = None
    privacy_level: Optional[PrivacyLevel] = None
    data: Optional[Dict[str, Any]] = None


class UserSettingsResponse(UserSettingsBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ================================
# List Responses
# ================================

class UserFavoriteListResponse(BaseModel):
    total: int
    items: List[UserFavoriteResponse]


class UserContributionListResponse(BaseModel):
    total: int
    items: List[UserContributionResponse]


class UserActivityListResponse(BaseModel):
    total: int
    items: List[UserActivityResponse]
