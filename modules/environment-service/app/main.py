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

"""
Environment Service - Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from .config import settings
from .routes import air_quality_router, weather_router

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
    logger.info(f"OpenAQ API: {settings.OPENAQ_API_URL}")
    logger.info(f"OpenWeather API configured: {bool(settings.OPENWEATHER_API_KEY)}")
    
    # Connect to message brokers
    from .messaging import rabbitmq_publisher, mqtt_handler
    
    # Connect to RabbitMQ
    rabbitmq_connected = await rabbitmq_publisher.connect()
    if rabbitmq_connected:
        logger.info("RabbitMQ publisher ready")
    else:
        logger.warning("RabbitMQ not available - events will not be published")
    
    # Start MQTT subscriber
    await mqtt_handler.start_subscriber()
    logger.info("MQTT subscriber started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Environment Service")
    
    # Stop MQTT subscriber
    await mqtt_handler.stop_subscriber()
    
    # Close RabbitMQ
    await rabbitmq_publisher.close()
    
    # Close HTTP clients
    from .clients import openaq_client, openweather_client
    await openaq_client.close()
    await openweather_client.close()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="OpenAQ and OpenWeather API integration for GreenEduMap",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(air_quality_router)
app.include_router(weather_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "messaging": {
            "rabbitmq": settings.RABBITMQ_URL.split("@")[-1] if "@" in settings.RABBITMQ_URL else "configured",
            "mqtt": f"{settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from .messaging import rabbitmq_publisher
    
    return {
        "status": "healthy",
        "service": "environment-service",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "messaging": {
            "rabbitmq": "connected" if rabbitmq_publisher.connection else "disconnected",
            "mqtt": "configured"
        }
    }


# API endpoint to trigger AI analysis
@app.post("/api/v1/trigger-analysis")
async def trigger_ai_analysis(analysis_type: str = "clustering"):
    """Trigger AI analysis via RabbitMQ"""
    from .messaging import rabbitmq_publisher
    
    if analysis_type == "clustering":
        await rabbitmq_publisher.request_ai_clustering(
            data_type="environment",
            parameters={"n_clusters": 3, "method": "kmeans"}
        )
    elif analysis_type == "correlation":
        await rabbitmq_publisher.request_ai_correlation(
            environment_ids=[],
            education_ids=[],
            analysis_type="pearson"
        )
    
    return {"status": "queued", "analysis_type": analysis_type}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
