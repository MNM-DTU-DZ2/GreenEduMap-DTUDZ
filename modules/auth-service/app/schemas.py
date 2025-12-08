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

"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, UUID4
from enum import Enum


class UserRole(str, Enum):
    """User role enum."""
    ADMIN = "admin"
    VOLUNTEER = "volunteer"
    CITIZEN = "citizen"
    DEVELOPER = "developer"
    SCHOOL = "school"


# ================================
# User Schemas
# ================================

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CITIZEN


class UserUpdate(BaseModel):
    """Schema for user update."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_public: Optional[bool] = None


class UserInDB(UserBase):
    """User schema with DB fields."""
    id: UUID4
    role: str
    is_active: bool
    is_verified: bool
    is_public: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """User response schema (public)."""
    id: UUID4
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ================================
# Auth Schemas
# ================================

class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes


class TokenRefreshRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: str  # user_id
    email: str
    role: str
    exp: datetime
    iat: datetime
    type: str  # access|refresh


class TokenValidationResponse(BaseModel):
    """Token validation response."""
    valid: bool
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    expires_at: Optional[datetime] = None


# ================================
# API Key Schemas
# ================================

class APIKeyCreate(BaseModel):
    """API key creation schema."""
    name: str = Field(..., min_length=3, max_length=100)
    scopes: Optional[str] = "read"
    rate_limit: int = 1000


class APIKeyResponse(BaseModel):
    """API key response (includes plain key once)."""
    id: UUID4
    name: str
    api_key: str  # Only returned once!
    key_prefix: str
    scopes: Optional[str]
    rate_limit: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class APIKeyInfo(BaseModel):
    """API key info (without plain key)."""
    id: UUID4
    name: str
    key_prefix: str
    scopes: Optional[str]
    rate_limit: int
    is_active: bool
    total_requests: int
    last_used: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ================================
# Generic Responses
# ================================

class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
