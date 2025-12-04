"""
RabbitMQ Client for GreenEduMap
Handles async message publishing and consuming
"""
import json
import asyncio
import logging
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass
import aio_pika
from aio_pika import ExchangeType, Message, DeliveryMode

logger = logging.getLogger(__name__)


@dataclass
class QueueConfig:
    """Queue configuration"""
    name: str
    exchange: str
    routing_key: str
    durable: bool = True
    auto_delete: bool = False


# Pre-defined exchanges and queues for GreenEduMap
class Exchanges:
    ENVIRONMENT_EVENTS = "environment.events"
    EDUCATION_EVENTS = "education.events"
    AI_TASKS = "ai.tasks"
    NOTIFICATIONS = "notifications"
    EXPORT_TASKS = "export.tasks"


class Queues:
    AI_CLUSTERING = QueueConfig(
        name="ai.clustering.queue",
        exchange=Exchanges.AI_TASKS,
        routing_key="ai.clustering"
    )
    AI_PREDICTION = QueueConfig(
        name="ai.prediction.queue",
        exchange=Exchanges.AI_TASKS,
        routing_key="ai.prediction"
    )
    AI_CORRELATION = QueueConfig(
        name="ai.correlation.queue",
        exchange=Exchanges.AI_TASKS,
        routing_key="ai.correlation"
    )
    EXPORT_CSV = QueueConfig(
        name="export.csv.queue",
        exchange=Exchanges.EXPORT_TASKS,
        routing_key="export.csv"
    )
    EXPORT_GEOJSON = QueueConfig(
        name="export.geojson.queue",
        exchange=Exchanges.EXPORT_TASKS,
        routing_key="export.geojson"
    )
    NOTIFICATION_EMAIL = QueueConfig(
        name="notification.email.queue",
        exchange=Exchanges.NOTIFICATIONS,
        routing_key="notification.email"
    )
    NOTIFICATION_PUSH = QueueConfig(
        name="notification.push.queue",
        exchange=Exchanges.NOTIFICATIONS,
        routing_key="notification.push"
    )


class RabbitMQClient:
    """Base RabbitMQ client with connection management"""
    
    def __init__(self, url: str):
        self.url = url
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self._exchanges: Dict[str, aio_pika.Exchange] = {}
    
    async def connect(self) -> None:
        """Establish connection to RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)
            logger.info("Connected to RabbitMQ successfully")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    async def close(self) -> None:
        """Close connection"""
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")
    
    async def declare_exchange(
        self, 
        name: str, 
        exchange_type: ExchangeType = ExchangeType.TOPIC,
        durable: bool = True
    ) -> aio_pika.Exchange:
        """Declare an exchange"""
        if name not in self._exchanges:
            exchange = await self.channel.declare_exchange(
                name,
                exchange_type,
                durable=durable
            )
            self._exchanges[name] = exchange
            logger.info(f"Declared exchange: {name}")
        return self._exchanges[name]
    
    async def declare_queue(self, config: QueueConfig) -> aio_pika.Queue:
        """Declare a queue and bind to exchange"""
        queue = await self.channel.declare_queue(
            config.name,
            durable=config.durable,
            auto_delete=config.auto_delete
        )
        
        exchange = await self.declare_exchange(config.exchange)
        await queue.bind(exchange, routing_key=config.routing_key)
        
        logger.info(f"Declared queue: {config.name} bound to {config.exchange}")
        return queue


class RabbitMQPublisher(RabbitMQClient):
    """Publisher for sending messages to RabbitMQ"""
    
    async def publish(
        self,
        exchange_name: str,
        routing_key: str,
        message: Dict[str, Any],
        persistent: bool = True
    ) -> None:
        """Publish a message to an exchange"""
        try:
            exchange = await self.declare_exchange(exchange_name)
            
            body = json.dumps(message, default=str).encode()
            
            await exchange.publish(
                Message(
                    body,
                    delivery_mode=DeliveryMode.PERSISTENT if persistent else DeliveryMode.NOT_PERSISTENT,
                    content_type="application/json"
                ),
                routing_key=routing_key
            )
            
            logger.debug(f"Published message to {exchange_name}/{routing_key}")
            
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
    
    async def publish_environment_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Publish environment-related event"""
        message = {
            "event_type": event_type,
            "data": data
        }
        await self.publish(
            Exchanges.ENVIRONMENT_EVENTS,
            f"environment.{event_type}",
            message
        )
    
    async def publish_ai_task(self, task_type: str, data: Dict[str, Any]) -> None:
        """Publish AI processing task"""
        message = {
            "task_type": task_type,
            "data": data
        }
        await self.publish(
            Exchanges.AI_TASKS,
            f"ai.{task_type}",
            message
        )
    
    async def publish_export_task(self, format_type: str, data: Dict[str, Any]) -> None:
        """Publish export task"""
        message = {
            "format": format_type,
            "data": data
        }
        await self.publish(
            Exchanges.EXPORT_TASKS,
            f"export.{format_type}",
            message
        )


class RabbitMQConsumer(RabbitMQClient):
    """Consumer for receiving messages from RabbitMQ"""
    
    def __init__(self, url: str):
        super().__init__(url)
        self._consumers: Dict[str, asyncio.Task] = {}
    
    async def consume(
        self,
        queue_config: QueueConfig,
        callback: Callable[[Dict[str, Any]], Any],
        auto_ack: bool = False
    ) -> None:
        """Start consuming messages from a queue"""
        queue = await self.declare_queue(queue_config)
        
        async def process_message(message: aio_pika.IncomingMessage):
            async with message.process(ignore_processed=True):
                try:
                    body = json.loads(message.body.decode())
                    await callback(body)
                    if not auto_ack:
                        await message.ack()
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await message.nack(requeue=True)
        
        await queue.consume(process_message)
        logger.info(f"Started consuming from queue: {queue_config.name}")
    
    async def stop_consuming(self) -> None:
        """Stop all consumers"""
        for task in self._consumers.values():
            task.cancel()
        self._consumers.clear()
        logger.info("Stopped all consumers")

