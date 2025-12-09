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
Clustering Consumer - Listen for clustering tasks from RabbitMQ
"""
import json
import logging
from aio_pika import connect_robust, IncomingMessage
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.clustering import EnvironmentClustering
from app.utils.data_loader import load_combined_data

logger = logging.getLogger(__name__)


async def process_clustering_task(message: IncomingMessage):
    """
    Process clustering task from queue
    
    Args:
        message: RabbitMQ message
    """
    async with message.process():
        try:
            # Parse message
            body = json.loads(message.body.decode())
            task_id = body.get('task_id')
            data_type = body.get('data', {}).get('task_type', 'environment')
            n_clusters = body.get('data', {}).get('parameters', {}).get('n_clusters', 3)
            
            logger.info(f"Processing clustering task {task_id}: type={data_type}, n_clusters={n_clusters}")
            
            # Load data from database
            async with AsyncSessionLocal() as db:
                combined_data = await load_combined_data(db)
                
                env_data = combined_data['environment']
                edu_data = combined_data['education']
                
                # Merge data for clustering
                # Use schools data with nearest AQI measurements
                merged_data = []
                for school in edu_data:
                    # Find nearest AQI measurement (simplified)
                    if env_data:
                        closest_env = min(env_data, key=lambda e: 
                            ((e['latitude'] - school['latitude'])**2 + 
                             (e['longitude'] - school['longitude'])**2)**0.5
                        )
                        
                        merged_data.append({
                            'id': school['id'],
                            'name': school['name'],
                            'latitude': school['latitude'],
                            'longitude': school['longitude'],
                            'green_score': school['green_score'],
                            'aqi': closest_env['aqi']
                        })
                
                if not merged_data:
                    logger.warning(f"No data available for clustering task {task_id}")
                    return
                
                # Run clustering
                clustering = EnvironmentClustering(n_clusters=n_clusters)
                results = clustering.fit_predict(merged_data)
                stats = clustering.get_cluster_stats(results)
                
                logger.info(f"Clustering completed for task {task_id}: {stats}")
                
                # TODO: Store results in database or publish to another queue
                # For now, just log the results
                logger.info(f"Clustering results: {len(results)} points assigned to {n_clusters} zones")
                logger.info(f"Zone distribution: {stats}")
                
        except Exception as e:
            logger.error(f"Error processing clustering task: {e}", exc_info=True)


async def start_clustering_consumer():
    """Start RabbitMQ consumer for clustering tasks"""
    try:
        connection = await connect_robust(settings.RABBITMQ_URL)
        channel = await connection.channel()
        
        # Declare exchange and queue
        exchange = await channel.declare_exchange('ai.tasks', 'direct', durable=True)
        queue = await channel.declare_queue('ai.clustering.queue', durable=True)
        await queue.bind(exchange, routing_key='ai.clustering')
        
        # Start consuming
        await queue.consume(process_clustering_task)
        
        logger.info("Clustering consumer started, waiting for tasks...")
        
        return connection
        
    except Exception as e:
        logger.error(f"Error starting clustering consumer: {e}", exc_info=True)
        raise

