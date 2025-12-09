#!/usr/bin/env python3
"""
GreenEduMap-DTUDZ - User Data Models
Models for user favorites, contributions, activities, settings
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from geoalchemy2 import Geography
from app.core.database import Base


class UserFavorite(Base):
    """User favorite locations model."""
    
    __tablename__ = "user_favorites"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_type = Column(String(50), nullable=False)  # school, green_zone, recycling_center
    target_id = Column(UUID(as_uuid=True), nullable=False)
    note = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserFavorite {self.target_type}:{self.target_id}>"


class UserContribution(Base):
    """User contribution model (AQI reports, green spots, issues)."""
    
    __tablename__ = "user_contributions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # aqi_report, green_spot, issue, feedback
    title = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(Geography(geometry_type='POINT', srid=4326))
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    address = Column(Text)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    is_public = Column(Boolean, default=True)
    data = Column(JSONB)  # Additional data
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserContribution {self.type}: {self.title}>"


class UserActivity(Base):
    """User activity log model."""
    
    __tablename__ = "user_activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String(100), nullable=False)  # login, view, create, update, delete, share
    target_type = Column(String(50))
    target_id = Column(UUID(as_uuid=True))
    description = Column(Text)
    extra_data = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserActivity {self.action} by {self.user_id}>"


class UserSettings(Base):
    """User settings model."""
    
    __tablename__ = "user_settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    notification_enabled = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    language = Column(String(10), default="vi")
    theme = Column(String(20), default="light")
    default_city = Column(String(100), default="TP. Hồ Chí Minh")
    default_latitude = Column(DECIMAL(10, 7), default=10.7769)
    default_longitude = Column(DECIMAL(10, 7), default=106.7009)
    privacy_level = Column(String(20), default="public")  # public, friends, private
    data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserSettings for {self.user_id}>"
