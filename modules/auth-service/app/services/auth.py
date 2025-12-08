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

"""Authentication service - JWT and session management."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models import User, RefreshToken, APIKey
from app.schemas import UserCreate, LoginRequest, TokenResponse
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_api_key,
    hash_api_key,
)
from app.core.config import settings


class AuthService:
    """Authentication service class."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def register_user(self, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check if email exists
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username exists
        result = await self.db.execute(
            select(User).where(User.username == user_data.username)
        )
        existing_username = result.scalar_one_or_none()
        
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role.value,
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def authenticate_user(self, login_data: LoginRequest) -> Optional[User]:
        """Authenticate user with email and password."""
        result = await self.db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not verify_password(login_data.password, user.password_hash):
            return None
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()
        
        return user
    
    async def create_tokens(self, user: User) -> TokenResponse:
        """Create access and refresh tokens for user."""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
        
        access_token = create_access_token(token_data)
        refresh_token_str = create_refresh_token(token_data)
        
        # Store refresh token in database
        refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=get_password_hash(refresh_token_str),
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        
        self.db.add(refresh_token)
        await self.db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_str,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def refresh_access_token(self, refresh_token_str: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token_str)
        
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        
        # Get all refresh tokens for this user
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False
            )
        )
        stored_tokens = result.scalars().all()
        
        # Verify refresh token hash
        stored_token = None
        for token in stored_tokens:
            if verify_password(refresh_token_str, token.token_hash):
                stored_token = token
                break
        
        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found or revoked"
            )
        
        if stored_token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Get user
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create new tokens
        return await self.create_tokens(user)
    
    async def verify_access_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode access token."""
        payload = decode_token(token)
        
        if not payload or payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check expiration
        exp = payload.get("exp")
        if datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    
    async def create_api_key(self, user_id: str, name: str, scopes: str = "read", rate_limit: int = 1000) -> tuple[APIKey, str]:
        """Create new API key for developer."""
        # Generate API key
        plain_key = generate_api_key()
        key_hash = hash_api_key(plain_key)
        key_prefix = plain_key[:8]
        
        # Store in database
        api_key = APIKey(
            user_id=user_id,
            key_hash=key_hash,
            key_prefix=key_prefix,
            name=name,
            scopes=scopes,
            rate_limit=rate_limit,
        )
        
        self.db.add(api_key)
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return api_key, plain_key  # Return plain key only once!
    
    async def revoke_refresh_token(self, user_id: str, token_id: str):
        """Revoke a refresh token."""
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.id == token_id,
                RefreshToken.user_id == user_id
            )
        )
        token = result.scalar_one_or_none()
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token not found"
            )
        
        token.is_revoked = True
        await self.db.commit()
