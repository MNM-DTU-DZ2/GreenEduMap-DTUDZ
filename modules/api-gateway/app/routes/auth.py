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

"""Auth service proxy routes."""
from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

AUTH_SERVICE_URL = "http://auth-service:8001"

@router.get("/health")
async def health_check():
    """Health check proxy to auth service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{AUTH_SERVICE_URL}/health", timeout=5.0)
            return JSONResponse(
                content=response.json() if response.status_code == 200 else {"status": "error"},
                status_code=response.status_code
            )
        except httpx.RequestError:
            return JSONResponse(
                content={"status": "unavailable"},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request):
    """
    Register a new user.
    
    Proxies to auth-service: POST /api/v1/auth/register
    """
    body = await request.json()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/auth/register",
                json=body,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.post("/login")
async def login(request: Request):
    """
    User login.
    
    Proxies to auth-service: POST /api/v1/auth/login
    """
    body = await request.json()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/auth/login",
                json=body,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.post("/refresh")
async def refresh_token(request: Request):
    """
    Refresh access token.
    
    Proxies to auth-service: POST /api/v1/auth/refresh
    """
    body = await request.json()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/auth/refresh",
                json=body,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get("/me")
async def get_current_user(request: Request):
    """
    Get current logged-in user.
    
    Proxies to auth-service: GET /api/v1/auth/me
    Requires: Authorization Bearer token
    """
    # Forward auth header
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/auth/me",
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.patch("/profile")
async def update_profile(request: Request):
    """
    Update user profile.
    
    Proxies to auth-service: PATCH /api/v1/auth/profile
    Requires: Authorization Bearer token
    """
    body = await request.json()
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            # Update profile directly using auth/profile endpoint
            response = await client.patch(
                f"{AUTH_SERVICE_URL}/api/v1/auth/profile",
                json=body,
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json() if response.status_code != 204 else {"message": "Profile updated"},
                status_code=response.status_code if response.status_code != 204 else 200,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get("/validate-token")
async def validate_token(request: Request):
    """
    Validate if access token is still valid.
    
    Proxies to auth-service: GET /api/v1/auth/validate-token
    Requires: Authorization Bearer token
    """
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/auth/validate-token",
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


# ================================
# FCM Token Management
# ================================

@router.post("/fcm-tokens", status_code=status.HTTP_201_CREATED)
async def register_fcm_token(request: Request):
    """
    Register FCM token for push notifications.
    
    Proxies to auth-service: POST /api/v1/fcm-tokens
    Requires: Authorization Bearer token
    """
    body = await request.json()
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/fcm-tokens",
                json=body,
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.post("/update-fcm-token", status_code=status.HTTP_201_CREATED)
async def update_fcm_token(request: Request):
    """
    Update FCM token (alias for POST /fcm-tokens for mobile compatibility).
    
    Proxies to auth-service: POST /api/v1/fcm-tokens
    Requires: Authorization Bearer token
    """
    body = await request.json()
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/fcm-tokens",
                json=body,
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get("/fcm-tokens")
async def list_fcm_tokens(request: Request):
    """
    List FCM tokens for current user.
    
    Proxies to auth-service: GET /api/v1/fcm-tokens
    Requires: Authorization Bearer token
    """
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/fcm-tokens",
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.delete("/fcm-tokens/{token_id}")
async def delete_fcm_token(request: Request, token_id: str):
    """
    Delete FCM token.
    
    Proxies to auth-service: DELETE /api/v1/fcm-tokens/{token_id}
    Requires: Authorization Bearer token
    """
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f"{AUTH_SERVICE_URL}/api/v1/fcm-tokens/{token_id}",
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json() if response.status_code != 204 else {"message": "Token deleted"},
                status_code=response.status_code if response.status_code != 204 else 200,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


# ================================
# Notifications
# ================================

@router.post("/notifications/send")
async def send_notification(request: Request):
    """
    Send push notification.
    
    Proxies to auth-service: POST /api/v1/notifications/send
    Requires: Authorization Bearer token
    """
    body = await request.json()
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/notifications/send",
                json=body,
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


# ================================
# User Management
# ================================

@router.get("/users")
async def list_users(request: Request):
    """
    List users (Admin only).
    
    Proxies to auth-service: GET /api/v1/users
    Requires: Authorization Bearer token (Admin)
    """
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/users",
                params=dict(request.query_params),
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get("/users/{user_id}")
async def get_user(request: Request, user_id: str):
    """
    Get user by ID.
    
    Proxies to auth-service: GET /api/v1/users/{user_id}
    Requires: Authorization Bearer token
    """
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/users/{user_id}",
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.delete("/users/{user_id}")
async def delete_user(request: Request, user_id: str):
    """
    Delete user (Admin only).
    
    Proxies to auth-service: DELETE /api/v1/users/{user_id}
    Requires: Authorization Bearer token (Admin)
    """
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f"{AUTH_SERVICE_URL}/api/v1/users/{user_id}",
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json() if response.status_code != 204 else {"message": "User deleted"},
                status_code=response.status_code if response.status_code != 204 else 200,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


# ================================
# API Keys
# ================================

@router.post("/api-keys")
async def create_api_key(request: Request):
    """
    Create API key (Developer/Admin).
    
    Proxies to auth-service: POST /api/v1/api-keys
    Requires: Authorization Bearer token (Developer/Admin)
    """
    body = await request.json()
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/api/v1/api-keys",
                json=body,
                headers=headers,
                timeout=10.0,
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": "Auth service unavailable", "detail": str(e)},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

