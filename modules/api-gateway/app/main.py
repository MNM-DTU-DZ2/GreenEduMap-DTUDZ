"""
API Gateway - Main Application
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional
import logging

from .config import settings
from .routes.public import router as public_router
from .routes.resources import router as resources_router
from .routes.education import router as education_router, opendata_router as education_opendata_router
from .routes.auth import router as auth_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment Service: {settings.ENVIRONMENT_SERVICE_URL}")
    logger.info(f"Auth Service: {settings.AUTH_SERVICE_URL}")
    logger.info(f"Education Service: {settings.EDUCATION_SERVICE_URL}")
    
    # Connect to RabbitMQ
    from .messaging import task_publisher
    rabbitmq_connected = await task_publisher.connect()
    if rabbitmq_connected:
        logger.info("RabbitMQ task publisher ready")
    else:
        logger.warning("RabbitMQ not available - async tasks will not work")
    
    yield
    
    # Shutdown
    logger.info("Shutting down API Gateway")
    await task_publisher.close()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Central API Gateway for GreenEduMap microservices",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
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
app.include_router(auth_router)


@app.get("/")
async def root():
    """Root endpoint"""
    from .messaging import task_publisher
    
    return {
        "service": "GreenEduMap API Gateway",
        "version": settings.VERSION,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "opendata": "/api/open-data",
            "health": "/health",
            "tasks": "/api/v1/tasks"
        },
        "messaging": {
            "rabbitmq": "connected" if task_publisher.is_connected else "disconnected"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint - aggregates health from all services
    """
    import httpx
    from .messaging import task_publisher
    
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
        "services": services_health,
        "messaging": {
            "rabbitmq": "connected" if task_publisher.is_connected else "disconnected"
        }
    }


# ================================
# Async Task Endpoints
# ================================

@app.post("/api/v1/tasks/ai/clustering")
async def queue_clustering_task(
    data_type: str = "environment",
    n_clusters: int = 3,
    method: str = "kmeans"
):
    """Queue AI clustering task"""
    from .messaging import task_publisher
    
    task_id = await task_publisher.queue_clustering_task(
        data_type=data_type,
        n_clusters=n_clusters,
        method=method
    )
    
    if task_id:
        return {"status": "queued", "task_id": task_id}
    return {"status": "failed", "error": "RabbitMQ not available"}


@app.post("/api/v1/tasks/ai/prediction")
async def queue_prediction_task(
    prediction_type: str = "air_quality",
    location_id: Optional[str] = None
):
    """Queue AI prediction task"""
    from .messaging import task_publisher
    
    task_id = await task_publisher.queue_prediction_task(
        prediction_type=prediction_type,
        location_id=location_id
    )
    
    if task_id:
        return {"status": "queued", "task_id": task_id}
    return {"status": "failed", "error": "RabbitMQ not available"}


@app.post("/api/v1/tasks/ai/correlation")
async def queue_correlation_task(
    analysis_type: str = "pearson"
):
    """Queue AI correlation analysis task"""
    from .messaging import task_publisher
    
    task_id = await task_publisher.queue_correlation_task(
        environment_ids=[],
        education_ids=[],
        analysis_type=analysis_type
    )
    
    if task_id:
        return {"status": "queued", "task_id": task_id}
    return {"status": "failed", "error": "RabbitMQ not available"}


@app.post("/api/v1/tasks/export")
async def queue_export_task(
    data_type: str = "schools",
    format: str = "csv"
):
    """Queue data export task"""
    from .messaging import task_publisher
    
    task_id = await task_publisher.queue_export_task(
        data_type=data_type,
        format=format
    )
    
    if task_id:
        return {"status": "queued", "task_id": task_id}
    return {"status": "failed", "error": "RabbitMQ not available"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
