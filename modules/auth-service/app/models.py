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

"""Database models for Auth Service."""
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry

from app.core.database import Base


class User(Base):
    """User model - OpenData compliant."""
    
    __tablename__ = "users"
    
    # Primary Key (UUID for OpenData)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(255))
    phone = Column(String(20))
    
    # Role-based Access Control
    role = Column(
        String(50),
        nullable=False,
        default="citizen",
        comment="admin|volunteer|citizen|developer|school"
    )
    
    # Location (PostGIS)
    location = Column(Geometry('POINT', srid=4326))
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # OpenData Fields
    is_public = Column(Boolean, default=False, nullable=False, comment="Allow public API access")
    profile_uri = Column(String(500), comment="Linked Data URI")
    
    # Metadata (extensibility)
    metadata_json = Column(Text, comment="Additional profile data")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.username} ({self.email})>"


class APIKey(Base):
    """API Key model for developers."""
    
    __tablename__ = "api_keys"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Owner
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # API Key
    key_hash = Column(String(255), nullable=False, unique=True)
    key_prefix = Column(String(20), nullable=False, comment="First 8 chars for identification")
    name = Column(String(100), nullable=False, comment="Key description")
    
    # Permissions
    scopes = Column(Text, comment="Comma-separated scopes: read,write,admin")
    rate_limit = Column(Integer, default=1000, comment="Requests per hour")
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Usage Stats
    total_requests = Column(Integer, default=0)
    last_used = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, comment="Optional expiration")
    
    def __repr__(self):
        return f"<APIKey {self.name} (prefix: {self.key_prefix})>"


class RefreshToken(Base):
    """Refresh token model for JWT rotation."""
    
    __tablename__ = "refresh_tokens"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Owner
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Token
    token_hash = Column(String(255), nullable=False, unique=True)
    
    # Device Info
    device_name = Column(String(100))
    ip_address = Column(String(50))
    user_agent = Column(Text)
    
    # Status
    is_revoked = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    last_used = Column(DateTime)
    
    def __repr__(self):
        return f"<RefreshToken user_id={self.user_id}>"
