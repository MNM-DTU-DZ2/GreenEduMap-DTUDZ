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
)
from app.services.auth import AuthService
from app.services.user import UserService
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await init_db()
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
    - **username**: Username (unique, 3-50 chars)
    - **password**: Strong password (min 8 chars)
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
