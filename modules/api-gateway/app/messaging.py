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
Messaging module for API Gateway
Handles RabbitMQ publishing for async tasks
"""
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

import aio_pika
from aio_pika import ExchangeType, Message, DeliveryMode

from .config import settings

logger = logging.getLogger(__name__)


class TaskPublisher:
    """RabbitMQ publisher for async tasks"""
    
    def __init__(self):
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self._exchanges: Dict[str, aio_pika.Exchange] = {}
        self._connected = False
    
    @property
    def is_connected(self) -> bool:
        return self._connected
    
    async def connect(self) -> bool:
        """Connect to RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()
            
            # Declare exchanges
            exchanges = [
                ("ai.tasks", ExchangeType.DIRECT),
                ("export.tasks", ExchangeType.DIRECT),
                ("notifications", ExchangeType.TOPIC),
            ]
            
            for name, ex_type in exchanges:
                exchange = await self.channel.declare_exchange(
                    name, ex_type, durable=True
                )
                self._exchanges[name] = exchange
            
            self._connected = True
            logger.info("Connected to RabbitMQ successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Failed to connect to RabbitMQ: {e}")
            self._connected = False
            return False
    
    async def close(self):
        """Close connection"""
        if self.connection:
            await self.connection.close()
            self._connected = False
            logger.info("RabbitMQ connection closed")
    
    async def _publish(
        self,
        exchange: str,
        routing_key: str,
        message: Dict[str, Any]
    ) -> Optional[str]:
        """Publish message to exchange"""
        if not self._connected:
            logger.warning("RabbitMQ not connected")
            return None
        
        try:
            task_id = str(uuid.uuid4())
            message["task_id"] = task_id
            message["timestamp"] = datetime.utcnow().isoformat() + "Z"
            message["source"] = "api-gateway"
            
            ex = self._exchanges.get(exchange)
            if not ex:
                logger.error(f"Exchange {exchange} not found")
                return None
            
            await ex.publish(
                Message(
                    json.dumps(message, default=str).encode(),
                    delivery_mode=DeliveryMode.PERSISTENT,
                    content_type="application/json",
                    message_id=task_id
                ),
                routing_key=routing_key
            )
            
            logger.info(f"Published task {task_id} to {exchange}/{routing_key}")
            return task_id
            
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return None
    
    # ================================
    # AI Tasks
    # ================================
    
    async def queue_clustering_task(
        self,
        data_type: str,
        n_clusters: int = 3,
        method: str = "kmeans",
        **kwargs
    ) -> Optional[str]:
        """Queue AI clustering task"""
        return await self._publish(
            "ai.tasks",
            "ai.clustering",
            {
                "task_type": "clustering",
                "data_type": data_type,
                "parameters": {
                    "n_clusters": n_clusters,
                    "method": method,
                    **kwargs
                }
            }
        )
    
    async def queue_prediction_task(
        self,
        prediction_type: str,
        location_id: Optional[str] = None,
        **kwargs
    ) -> Optional[str]:
        """Queue AI prediction task"""
        return await self._publish(
            "ai.tasks",
            "ai.prediction",
            {
                "task_type": "prediction",
                "prediction_type": prediction_type,
                "location_id": location_id,
                "parameters": kwargs
            }
        )
    
    async def queue_correlation_task(
        self,
        environment_ids: list,
        education_ids: list,
        analysis_type: str = "pearson"
    ) -> Optional[str]:
        """Queue AI correlation analysis task"""
        return await self._publish(
            "ai.tasks",
            "ai.correlation",
            {
                "task_type": "correlation",
                "environment_data_ids": environment_ids,
                "education_data_ids": education_ids,
                "analysis_type": analysis_type
            }
        )
    
    # ================================
    # Export Tasks
    # ================================
    
    async def queue_export_task(
        self,
        data_type: str,
        format: str,
        filters: Optional[Dict] = None,
        callback_url: Optional[str] = None
    ) -> Optional[str]:
        """Queue data export task"""
        return await self._publish(
            "export.tasks",
            f"export.{format}",
            {
                "task_type": "export",
                "data_type": data_type,
                "format": format,
                "filters": filters or {},
                "callback_url": callback_url
            }
        )
    
    # ================================
    # Notification Tasks
    # ================================
    
    async def queue_notification(
        self,
        notification_type: str,
        recipients: list,
        subject: str,
        content: str,
        **kwargs
    ) -> Optional[str]:
        """Queue notification"""
        return await self._publish(
            "notifications",
            f"notification.{notification_type}",
            {
                "task_type": "notification",
                "notification_type": notification_type,
                "recipients": recipients,
                "subject": subject,
                "content": content,
                **kwargs
            }
        )


# Global instance
task_publisher = TaskPublisher()

