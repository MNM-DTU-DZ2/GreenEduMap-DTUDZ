"""
Messaging module for Environment Service
Handles MQTT subscriptions and RabbitMQ publishing
"""
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime

import aio_pika
from aio_pika import ExchangeType, Message, DeliveryMode

try:
    import aiomqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False

from .config import settings

logger = logging.getLogger(__name__)


# ================================
# RabbitMQ Publisher
# ================================

class RabbitMQPublisher:
    """RabbitMQ publisher for environment events"""
    
    def __init__(self):
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self._exchanges: Dict[str, aio_pika.Exchange] = {}
    
    async def connect(self) -> bool:
        """Connect to RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()
            
            # Declare exchanges
            await self._declare_exchanges()
            
            logger.info("Connected to RabbitMQ successfully")
            return True
        except Exception as e:
            logger.warning(f"Failed to connect to RabbitMQ: {e}")
            return False
    
    async def _declare_exchanges(self):
        """Declare required exchanges"""
        exchanges = [
            ("environment.events", ExchangeType.FANOUT),
            ("ai.tasks", ExchangeType.DIRECT),
            ("notifications", ExchangeType.TOPIC),
        ]
        
        for name, ex_type in exchanges:
            exchange = await self.channel.declare_exchange(
                name, ex_type, durable=True
            )
            self._exchanges[name] = exchange
            logger.debug(f"Declared exchange: {name}")
    
    async def close(self):
        """Close connection"""
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")
    
    async def publish_event(
        self,
        exchange: str,
        routing_key: str,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Publish an event to RabbitMQ"""
        if not self.channel:
            logger.warning("RabbitMQ not connected, skipping publish")
            return
        
        try:
            message_body = {
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "environment-service",
                "data": data
            }
            
            ex = self._exchanges.get(exchange)
            if not ex:
                logger.error(f"Exchange {exchange} not found")
                return
            
            await ex.publish(
                Message(
                    json.dumps(message_body, default=str).encode(),
                    delivery_mode=DeliveryMode.PERSISTENT,
                    content_type="application/json"
                ),
                routing_key=routing_key
            )
            logger.debug(f"Published event {event_type} to {exchange}/{routing_key}")
            
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
    
    async def publish_air_quality_update(self, data: Dict[str, Any]):
        """Publish air quality update event"""
        await self.publish_event(
            "environment.events",
            "air_quality.updated",
            "air_quality.updated",
            data
        )
        
        # Check for alerts
        aqi = data.get("aqi", 0)
        if aqi >= settings.AQI_CRITICAL_THRESHOLD:
            await self.publish_alert("critical", "air_quality", data)
        elif aqi >= settings.AQI_WARNING_THRESHOLD:
            await self.publish_alert("warning", "air_quality", data)
    
    async def publish_weather_update(self, data: Dict[str, Any]):
        """Publish weather update event"""
        await self.publish_event(
            "environment.events",
            "weather.updated",
            "weather.updated",
            data
        )
    
    async def publish_alert(self, severity: str, alert_type: str, data: Dict[str, Any]):
        """Publish environment alert"""
        await self.publish_event(
            "notifications",
            f"alert.{severity}",
            f"environment.alert.{alert_type}",
            {
                "severity": severity,
                "alert_type": alert_type,
                **data
            }
        )
        logger.warning(f"Published {severity} alert for {alert_type}")
    
    async def request_ai_clustering(self, data_type: str, parameters: Dict[str, Any]):
        """Request AI clustering analysis"""
        await self.publish_event(
            "ai.tasks",
            "ai.clustering",
            "ai.clustering.requested",
            {
                "data_type": data_type,
                "parameters": parameters
            }
        )
    
    async def request_ai_correlation(
        self,
        environment_ids: list,
        education_ids: list,
        analysis_type: str = "pearson"
    ):
        """Request AI correlation analysis"""
        await self.publish_event(
            "ai.tasks",
            "ai.correlation",
            "ai.correlation.requested",
            {
                "environment_data_ids": environment_ids,
                "education_data_ids": education_ids,
                "analysis_type": analysis_type
            }
        )


# ================================
# MQTT Subscriber & Publisher
# ================================

class MQTTHandler:
    """MQTT handler for sensor data"""
    
    def __init__(self, rabbitmq_publisher: Optional[RabbitMQPublisher] = None):
        self.rabbitmq = rabbitmq_publisher
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start_subscriber(self):
        """Start MQTT subscriber for sensor data"""
        if not MQTT_AVAILABLE:
            logger.warning("aiomqtt not available, MQTT subscriber disabled")
            return
        
        self._running = True
        self._task = asyncio.create_task(self._subscribe_loop())
        logger.info("MQTT subscriber started")
    
    async def stop_subscriber(self):
        """Stop MQTT subscriber"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("MQTT subscriber stopped")
    
    async def _subscribe_loop(self):
        """Main subscription loop"""
        topics = [
            "sensors/air-quality/#",
            "sensors/weather/#",
            "sensors/energy/#",
        ]
        
        while self._running:
            try:
                async with aiomqtt.Client(
                    hostname=settings.MQTT_BROKER_HOST,
                    port=settings.MQTT_BROKER_PORT,
                    username=settings.MQTT_USERNAME,
                    password=settings.MQTT_PASSWORD,
                    identifier=f"{settings.MQTT_CLIENT_ID}-sub"
                ) as client:
                    for topic in topics:
                        await client.subscribe(topic)
                        logger.info(f"Subscribed to MQTT topic: {topic}")
                    
                    async for message in client.messages:
                        await self._handle_sensor_message(message)
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"MQTT connection error: {e}")
                if self._running:
                    await asyncio.sleep(5)  # Retry after 5 seconds
    
    async def _handle_sensor_message(self, message):
        """Handle incoming sensor message"""
        topic = str(message.topic)
        
        try:
            payload = json.loads(message.payload.decode())
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON from {topic}")
            return
        
        logger.debug(f"Received sensor data from {topic}")
        
        # Route to appropriate handler
        if "air-quality" in topic:
            await self._handle_air_quality_sensor(payload)
        elif "weather" in topic:
            await self._handle_weather_sensor(payload)
        elif "energy" in topic:
            await self._handle_energy_sensor(payload)
    
    async def _handle_air_quality_sensor(self, data: Dict[str, Any]):
        """Process air quality sensor data"""
        logger.info(f"Processing AQI data: {data.get('location_id', 'unknown')}")
        
        # TODO: Store to database
        
        # Publish to RabbitMQ for other services
        if self.rabbitmq:
            await self.rabbitmq.publish_air_quality_update(data)
        
        # Publish real-time update via MQTT
        await self.publish_realtime_update("aqi", data)
    
    async def _handle_weather_sensor(self, data: Dict[str, Any]):
        """Process weather sensor data"""
        logger.info(f"Processing weather data: {data.get('location_id', 'unknown')}")
        
        # TODO: Store to database
        
        # Publish to RabbitMQ
        if self.rabbitmq:
            await self.rabbitmq.publish_weather_update(data)
        
        # Publish real-time update
        await self.publish_realtime_update("weather", data)
    
    async def _handle_energy_sensor(self, data: Dict[str, Any]):
        """Process energy sensor data"""
        logger.info(f"Processing energy data: {data.get('school_id', 'unknown')}")
        # TODO: Implement energy data processing
    
    async def publish_realtime_update(self, update_type: str, data: Dict[str, Any]):
        """Publish real-time update to frontend via MQTT"""
        if not MQTT_AVAILABLE:
            return
        
        try:
            async with aiomqtt.Client(
                hostname=settings.MQTT_BROKER_HOST,
                port=settings.MQTT_BROKER_PORT,
                username=settings.MQTT_USERNAME,
                password=settings.MQTT_PASSWORD,
                identifier=f"{settings.MQTT_CLIENT_ID}-pub"
            ) as client:
                location_id = data.get("location_id", "all")
                topic = f"realtime/{update_type}/{location_id}"
                
                await client.publish(
                    topic,
                    json.dumps(data, default=str),
                    qos=1
                )
                logger.debug(f"Published realtime update to {topic}")
                
        except Exception as e:
            logger.error(f"Failed to publish realtime update: {e}")
    
    async def publish_map_update(self, data: Dict[str, Any]):
        """Publish map update for frontend"""
        if not MQTT_AVAILABLE:
            return
        
        try:
            async with aiomqtt.Client(
                hostname=settings.MQTT_BROKER_HOST,
                port=settings.MQTT_BROKER_PORT,
                username=settings.MQTT_USERNAME,
                password=settings.MQTT_PASSWORD,
                identifier=f"{settings.MQTT_CLIENT_ID}-map"
            ) as client:
                await client.publish(
                    "realtime/map/update",
                    json.dumps(data, default=str),
                    qos=1
                )
                
        except Exception as e:
            logger.error(f"Failed to publish map update: {e}")


# ================================
# Global instances
# ================================

rabbitmq_publisher = RabbitMQPublisher()
mqtt_handler = MQTTHandler(rabbitmq_publisher)

