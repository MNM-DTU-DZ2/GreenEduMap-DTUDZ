#!/usr/bin/env python3
"""
GreenEduMap-DTUDZ - User Data API Gateway Routes
Proxy routes for user favorites, contributions, activities, settings
"""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional

router = APIRouter(prefix="/api/v1/user-data", tags=["User Data"])

AUTH_SERVICE_URL = "http://auth-service:8001"


async def proxy_to_auth(
    request: Request,
    method: str,
    endpoint: str,
    body: Optional[dict] = None,
    params: Optional[dict] = None,
):
    """Generic proxy function to auth service."""
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    async with httpx.AsyncClient() as client:
        try:
            url = f"{AUTH_SERVICE_URL}/api/v1/user-data{endpoint}"
            
            if method == "GET":
                response = await client.get(url, headers=headers, params=params, timeout=10.0)
            elif method == "POST":
                response = await client.post(url, json=body, headers=headers, timeout=10.0)
            elif method == "PUT":
                response = await client.put(url, json=body, headers=headers, timeout=10.0)
            elif method == "PATCH":
                response = await client.patch(url, json=body, headers=headers, timeout=10.0)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, timeout=10.0)
            else:
                return JSONResponse(
                    content={"error": "Unsupported method"},
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                )
            
            if response.status_code == 204:
                return JSONResponse(content={"message": "Success"}, status_code=200)
            
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
# User Favorites
# ================================

@router.get("/favorites")
async def list_favorites(request: Request, skip: int = 0, limit: int = 50, target_type: Optional[str] = None):
    """Get current user's favorites list."""
    params = {"skip": skip, "limit": limit}
    if target_type:
        params["target_type"] = target_type
    return await proxy_to_auth(request, "GET", "/favorites", params=params)


@router.post("/favorites", status_code=status.HTTP_201_CREATED)
async def create_favorite(request: Request):
    """Add a new favorite location."""
    body = await request.json()
    return await proxy_to_auth(request, "POST", "/favorites", body=body)


@router.delete("/favorites/{favorite_id}")
async def delete_favorite(request: Request, favorite_id: str):
    """Remove a favorite."""
    return await proxy_to_auth(request, "DELETE", f"/favorites/{favorite_id}")


# ================================
# User Contributions
# ================================

@router.get("/contributions")
async def list_contributions(
    request: Request,
    skip: int = 0,
    limit: int = 50,
    type: Optional[str] = None,
    status_filter: Optional[str] = None,
):
    """Get current user's contributions."""
    params = {"skip": skip, "limit": limit}
    if type:
        params["type"] = type
    if status_filter:
        params["status"] = status_filter
    return await proxy_to_auth(request, "GET", "/contributions", params=params)


@router.get("/contributions/public")
async def list_public_contributions(
    request: Request,
    skip: int = 0,
    limit: int = 50,
    type: Optional[str] = None,
):
    """Get all public approved contributions."""
    params = {"skip": skip, "limit": limit}
    if type:
        params["type"] = type
    return await proxy_to_auth(request, "GET", "/contributions/public", params=params)


@router.post("/contributions", status_code=status.HTTP_201_CREATED)
async def create_contribution(request: Request):
    """Create a new contribution (AQI report, green spot, issue, feedback)."""
    body = await request.json()
    return await proxy_to_auth(request, "POST", "/contributions", body=body)


@router.get("/contributions/{contribution_id}")
async def get_contribution(request: Request, contribution_id: str):
    """Get a specific contribution."""
    return await proxy_to_auth(request, "GET", f"/contributions/{contribution_id}")


@router.patch("/contributions/{contribution_id}")
async def update_contribution(request: Request, contribution_id: str):
    """Update a contribution."""
    body = await request.json()
    return await proxy_to_auth(request, "PATCH", f"/contributions/{contribution_id}", body=body)


@router.patch("/contributions/{contribution_id}/review")
async def review_contribution(request: Request, contribution_id: str):
    """Review (approve/reject) a contribution. Admin only."""
    body = await request.json()
    return await proxy_to_auth(request, "PATCH", f"/contributions/{contribution_id}/review", body=body)


@router.delete("/contributions/{contribution_id}")
async def delete_contribution(request: Request, contribution_id: str):
    """Delete a contribution."""
    return await proxy_to_auth(request, "DELETE", f"/contributions/{contribution_id}")


# ================================
# User Activities
# ================================

@router.get("/activities")
async def list_activities(
    request: Request,
    skip: int = 0,
    limit: int = 50,
    action: Optional[str] = None,
):
    """Get current user's activity log."""
    params = {"skip": skip, "limit": limit}
    if action:
        params["action"] = action
    return await proxy_to_auth(request, "GET", "/activities", params=params)


@router.get("/activities/public/{user_id}")
async def list_user_public_activities(
    request: Request,
    user_id: str,
    skip: int = 0,
    limit: int = 20,
):
    """Get a user's public activities."""
    params = {"skip": skip, "limit": limit}
    return await proxy_to_auth(request, "GET", f"/activities/public/{user_id}", params=params)


@router.post("/activities", status_code=status.HTTP_201_CREATED)
async def create_activity(request: Request):
    """Log a new activity."""
    body = await request.json()
    return await proxy_to_auth(request, "POST", "/activities", body=body)


# ================================
# User Settings
# ================================

@router.get("/settings")
async def get_settings(request: Request):
    """Get current user's settings."""
    return await proxy_to_auth(request, "GET", "/settings")


@router.put("/settings")
async def update_settings(request: Request):
    """Update current user's settings."""
    body = await request.json()
    return await proxy_to_auth(request, "PUT", "/settings", body=body)
