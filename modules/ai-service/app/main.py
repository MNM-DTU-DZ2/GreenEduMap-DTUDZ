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
AI Service Main Application
Starts all RabbitMQ consumers for ML tasks
"""
import asyncio
import logging
from app.core.config import settings
from app.consumers.clustering_consumer import start_clustering_consumer
from app.consumers.prediction_consumer import start_prediction_consumer
from app.consumers.correlation_consumer import start_correlation_consumer

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def main():
    """Main function to start all consumers"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Database: {settings.DATABASE_URL}")
    logger.info(f"RabbitMQ: {settings.RABBITMQ_URL}")
    
    try:
        # Start all consumers
        logger.info("Starting AI consumers...")
        
        clustering_conn = await start_clustering_consumer()
        prediction_conn = await start_prediction_consumer()
        correlation_conn = await start_correlation_consumer()
        
        logger.info("✅ All AI consumers started successfully!")
        logger.info("🤖 AI Service is ready to process tasks")
        logger.info("Listening for:")
        logger.info("  - ai.clustering tasks")
        logger.info("  - ai.prediction tasks")
        logger.info("  - ai.correlation tasks")
        
        # Keep running
        await asyncio.Future()
        
    except KeyboardInterrupt:
        logger.info("Shutting down AI Service...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("AI Service stopped")

