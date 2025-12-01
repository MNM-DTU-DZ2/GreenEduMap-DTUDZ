"""
API Gateway - Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import settings
from .routes.public import router as public_router
from .routes.resources import router as resources_router
from .routes.education import router as education_router, opendata_router as education_opendata_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Central API Gateway for GreenEduMap microservices",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(public_router)
app.include_router(resources_router)
app.include_router(education_router)
app.include_router(education_opendata_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "GreenEduMap API Gateway",
        "version": settings.VERSION,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "opendata": "/api/open-data",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint - aggregates health from all services
    """
    import httpx
    
    services_health = {}
    
    # Check each service
    services = {
        "environment": f"{settings.ENVIRONMENT_SERVICE_URL}/health",
        "auth": f"{settings.AUTH_SERVICE_URL}/health",
        "education": f"{settings.EDUCATION_SERVICE_URL}/health",
        "resource": f"{settings.RESOURCE_SERVICE_URL}/health",
    }
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, url in services.items():
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    services_health[service_name] = "healthy"
                else:
                    services_health[service_name] = "unhealthy"
            except Exception as e:
                services_health[service_name] = f"unreachable: {str(e)}"
                logger.warning(f"Service {service_name} unreachable: {e}")
    
    all_healthy = all(status == "healthy" for status in services_health.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "gateway": "healthy",
        "services": services_health
    }


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment Service: {settings.ENVIRONMENT_SERVICE_URL}")
    logger.info(f"Auth Service: {settings.AUTH_SERVICE_URL}")
    logger.info(f"Education Service: {settings.EDUCATION_SERVICE_URL}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Shutting down API Gateway")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
