#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

"""Main FastAPI application for Auth Service."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List

from app.core.config import settings
from app.core.database import init_db, close_db, get_db
from app.dependencies import (
    get_auth_service,
    get_user_service,
    get_current_active_user,
    require_role,
)
from app.schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
    LoginRequest,
    TokenResponse,
    TokenRefreshRequest,
    MessageResponse,
    APIKeyCreate,
    APIKeyResponse,
    UserInDB,
    FCMTokenCreate,
    FCMTokenResponse,
    FCMTokenListResponse,
    NotificationRequest,
    NotificationResponse,
)
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.fcm import FCMService
from app.models import User
from app.core.firebase import init_firebase
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await init_db()
    init_firebase()  # Initialize Firebase on startup
    yield
    # Shutdown
    await close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Authentication and authorization service for GreenEduMap",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# Health Check
# ================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# ================================
# Authentication Endpoints
# ================================

@app.post("/api/v1/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(
    user_data: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    Register a new user.
    
    - **email**: Valid email address (unique)
    - **username**: Optional - auto-generated from email if not provided
    - **password**: Strong password (min 8 chars)
    - **full_name**: Optional - user's full name
    - **phone**: Optional - contact phone number
    - **role**: User role (citizen, volunteer, developer, school, admin)
    """
    user = await auth_service.register_user(user_data)
    return user


@app.post("/api/v1/auth/login", response_model=TokenResponse, tags=["Auth"])
async def login(
    login_data: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    Login with email and password.
    
    Returns JWT access token and refresh token.
    """
    user = await auth_service.authenticate_user(login_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    return await auth_service.create_tokens(user)


@app.post("/api/v1/auth/refresh", response_model=TokenResponse, tags=["Auth"])
async def refresh_token(
    refresh_data: TokenRefreshRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """
    Refresh access token using refresh token.
    """
    return await auth_service.refresh_access_token(refresh_data.refresh_token)


@app.get("/api/v1/auth/me", response_model=UserInDB, tags=["Auth"])
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get current logged-in user information.
    
    Requires: Bearer token in Authorization header
    """
    return current_user


@app.patch("/api/v1/auth/profile", response_model=UserResponse, tags=["Auth"])
async def update_profile(
    profile_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """
    Update current user's profile.
    
    Requires: Bearer token in Authorization header
    """
    updated_user = await user_service.update_user(
        user_id=current_user.id,
        user_data=profile_update
    )
    return updated_user


@app.get("/api/v1/auth/validate-token", tags=["Auth"])
async def validate_token(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Validate if the current access token is still valid.
    
    Returns user information if token is valid.
    Requires: Bearer token in Authorization header
    """
    from datetime import datetime
    return {
        "valid": True,
        "user_id": str(current_user.id),
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "checked_at": datetime.utcnow().isoformat()
    }



# ================================
# User Management Endpoints
# ================================


@app.get("/api/v1/users", response_model=List[UserResponse], tags=["Users"])
async def list_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(require_role("admin"))],  # Admin only
    skip: int = 0,
    limit: int = 100,
    role: str = None,
):
    """
    List all users (Admin only).
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    - **role**: Filter by role
    """
    users = await user_service.get_users(skip=skip, limit=limit, role=role)
    return users


@app.get("/api/v1/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(
    user_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get user by ID.
    
    Users can only view their own profile unless admin.
    """
    # Check permissions
    if str(current_user.id) != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@app.delete("/api/v1/users/{user_id}", response_model=MessageResponse, tags=["Users"])
async def delete_user(
    user_id: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(require_role("admin"))],  # Admin only
):
    """
    Delete user (Admin only).
    
    Soft delete - sets is_active = False
    """
    await user_service.delete_user(user_id)
    return MessageResponse(message="User deleted successfully")


# ================================
# API Key Management (Developers)
# ================================

@app.post("/api/v1/api-keys", response_model=APIKeyResponse, tags=["API Keys"])
async def create_api_key(
    key_data: APIKeyCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Create new API key for developers.
    
    **Warning**: The plain API key is only shown once! Store it securely.
    """
    if current_user.role not in ["developer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only developers and admins can create API keys"
        )
    
    api_key, plain_key = await auth_service.create_api_key(
        user_id=str(current_user.id),
        name=key_data.name,
        scopes=key_data.scopes,
        rate_limit=key_data.rate_limit,
    )
    
    # Return API key object with plain key (only once!)
    return APIKeyResponse(
        id=api_key.id,
        name=api_key.name,
        api_key=plain_key,  # Plain key - store this!
        key_prefix=api_key.key_prefix,
        scopes=api_key.scopes,
        rate_limit=api_key.rate_limit,
        created_at=api_key.created_at,
    )


# ================================
# FCM Token Management
# ================================

def get_fcm_service(db: AsyncSession = Depends(get_db)) -> FCMService:
    """Dependency to get FCM service instance."""
    return FCMService(db)


@app.post("/api/v1/fcm-tokens", response_model=FCMTokenResponse, status_code=status.HTTP_201_CREATED, tags=["FCM"])
async def register_fcm_token(
    token_data: FCMTokenCreate,
    fcm_service: Annotated[FCMService, Depends(get_fcm_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Register or update FCM token for push notifications.
    
    - **token**: FCM registration token from iOS/Android device
    - **device_type**: Platform (ios, android, web)
    - **device_name**: Optional device identifier
    - **device_id**: Optional unique device ID
    """
    fcm_token = await fcm_service.register_token(
        user_id=str(current_user.id),
        token=token_data.token,
        device_type=token_data.device_type.value,
        device_name=token_data.device_name,
        device_id=token_data.device_id,
    )
    return fcm_token


@app.get("/api/v1/fcm-tokens", response_model=FCMTokenListResponse, tags=["FCM"])
async def list_fcm_tokens(
    fcm_service: Annotated[FCMService, Depends(get_fcm_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    List all FCM tokens for current user.
    """
    tokens = await fcm_service.get_user_tokens(str(current_user.id), active_only=False)
    return FCMTokenListResponse(
        total=len(tokens),
        tokens=tokens
    )


@app.delete("/api/v1/fcm-tokens/{token_id}", response_model=MessageResponse, tags=["FCM"])
async def delete_fcm_token(
    token_id: str,
    fcm_service: Annotated[FCMService, Depends(get_fcm_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Deactivate an FCM token.
    """
    success = await fcm_service.remove_token(token_id, str(current_user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FCM token not found"
        )
    
    return MessageResponse(message="FCM token deactivated successfully")


@app.post("/api/v1/notifications/send", response_model=NotificationResponse, tags=["Notifications"])
async def send_push_notification(
    notification: NotificationRequest,
    fcm_service: Annotated[FCMService, Depends(get_fcm_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Send push notification to a user.
    
    - For regular users: sends to their own devices
    - For admins: can specify user_id to send to other users
    """
    # Determine target user
    target_user_id = notification.user_id
    
    if target_user_id is None:
        # Send to self
        target_user_id = current_user.id
    elif current_user.role != "admin":
        # Only admins can send to other users
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can send notifications to other users"
        )
    
    # Send notification
    result = await fcm_service.send_notification(
        user_id=str(target_user_id),
        title=notification.title,
        body=notification.body,
        data=notification.data.dict() if notification.data else None,
        image_url=notification.image_url,
        sound=notification.sound,
    )
    
    return NotificationResponse(**result)


# ================================
# Run Application
# ================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
