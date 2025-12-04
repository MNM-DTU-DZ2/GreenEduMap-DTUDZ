"""
MQTT Client for GreenEduMap
Handles IoT sensor data and real-time updates
"""
import json
import asyncio
import logging
from typing import Callable, Optional, Dict, Any, List
from dataclasses import dataclass
import aiomqtt

logger = logging.getLogger(__name__)


# MQTT Topics for GreenEduMap
class MQTTTopics:
    """Pre-defined MQTT topics"""
    # Sensor data (subscribe)
    SENSOR_AIR_QUALITY = "sensors/air-quality/+"  # + is wildcard for location_id
    SENSOR_WEATHER = "sensors/weather/+"
    SENSOR_ENERGY = "sensors/energy/+"
    SENSOR_ALL = "sensors/#"
    
    # Alerts (publish)
    ALERT_ENVIRONMENT = "alerts/environment/{severity}"
    ALERT_AIR_QUALITY = "alerts/air-quality/{location_id}"
    
    # Real-time updates (publish to frontend)
    REALTIME_AQI = "realtime/aqi/{location_id}"
    REALTIME_WEATHER = "realtime/weather/{location_id}"
    REALTIME_MAP = "realtime/map/update"
    
    # School data
    SCHOOL_GREEN_SCORE = "schools/green-score/{school_id}"
    SCHOOL_EVENTS = "schools/events/{school_id}"


@dataclass
class MQTTConfig:
    """MQTT connection configuration"""
    host: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    client_id: str = "greenedumap-client"
    keepalive: int = 60
    clean_session: bool = True


class MQTTClient:
    """Base MQTT client"""
    
    def __init__(self, config: MQTTConfig):
        self.config = config
        self.client: Optional[aiomqtt.Client] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Connect to MQTT broker"""
        try:
            self.client = aiomqtt.Client(
                hostname=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                identifier=self.config.client_id,
                keepalive=self.config.keepalive,
                clean_session=self.config.clean_session
            )
            self._connected = True
            logger.info(f"MQTT client configured for {self.config.host}:{self.config.port}")
        except Exception as e:
            logger.error(f"Failed to configure MQTT client: {e}")
            raise
    
    @property
    def is_connected(self) -> bool:
        return self._connected


class MQTTPublisher(MQTTClient):
    """Publisher for sending MQTT messages"""
    
    async def publish(
        self,
        topic: str,
        payload: Dict[str, Any],
        qos: int = 1,
        retain: bool = False
    ) -> None:
        """Publish a message to a topic"""
        try:
            async with aiomqtt.Client(
                hostname=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                identifier=f"{self.config.client_id}-pub"
            ) as client:
                message = json.dumps(payload, default=str)
                await client.publish(topic, message, qos=qos, retain=retain)
                logger.debug(f"Published to {topic}: {message[:100]}...")
        except Exception as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise
    
    async def publish_air_quality_update(
        self,
        location_id: str,
        aqi: float,
        pm25: float,
        pm10: float,
        **extra_data
    ) -> None:
        """Publish real-time AQI update"""
        topic = MQTTTopics.REALTIME_AQI.format(location_id=location_id)
        payload = {
            "location_id": location_id,
            "aqi": aqi,
            "pm25": pm25,
            "pm10": pm10,
            **extra_data
        }
        await self.publish(topic, payload)
    
    async def publish_weather_update(
        self,
        location_id: str,
        temperature: float,
        humidity: float,
        **extra_data
    ) -> None:
        """Publish real-time weather update"""
        topic = MQTTTopics.REALTIME_WEATHER.format(location_id=location_id)
        payload = {
            "location_id": location_id,
            "temperature": temperature,
            "humidity": humidity,
            **extra_data
        }
        await self.publish(topic, payload)
    
    async def publish_alert(
        self,
        severity: str,
        alert_type: str,
        message: str,
        location_id: Optional[str] = None,
        **extra_data
    ) -> None:
        """Publish environment alert"""
        topic = MQTTTopics.ALERT_ENVIRONMENT.format(severity=severity)
        payload = {
            "severity": severity,
            "alert_type": alert_type,
            "message": message,
            "location_id": location_id,
            **extra_data
        }
        await self.publish(topic, payload, qos=2)  # QoS 2 for important alerts
    
    async def publish_map_update(self, update_type: str, data: Dict[str, Any]) -> None:
        """Publish map update for frontend"""
        payload = {
            "update_type": update_type,
            "data": data
        }
        await self.publish(MQTTTopics.REALTIME_MAP, payload)


class MQTTSubscriber(MQTTClient):
    """Subscriber for receiving MQTT messages"""
    
    def __init__(self, config: MQTTConfig):
        super().__init__(config)
        self._callbacks: Dict[str, List[Callable]] = {}
        self._running = False
    
    def on_message(self, topic_pattern: str):
        """Decorator to register a callback for a topic pattern"""
        def decorator(func: Callable):
            if topic_pattern not in self._callbacks:
                self._callbacks[topic_pattern] = []
            self._callbacks[topic_pattern].append(func)
            return func
        return decorator
    
    def add_callback(self, topic_pattern: str, callback: Callable) -> None:
        """Add a callback for a topic pattern"""
        if topic_pattern not in self._callbacks:
            self._callbacks[topic_pattern] = []
        self._callbacks[topic_pattern].append(callback)
    
    async def start(self, topics: Optional[List[str]] = None) -> None:
        """Start listening to topics"""
        if topics is None:
            topics = list(self._callbacks.keys())
        
        if not topics:
            logger.warning("No topics to subscribe to")
            return
        
        self._running = True
        
        try:
            async with aiomqtt.Client(
                hostname=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                identifier=f"{self.config.client_id}-sub"
            ) as client:
                # Subscribe to all topics
                for topic in topics:
                    await client.subscribe(topic)
                    logger.info(f"Subscribed to topic: {topic}")
                
                # Process incoming messages
                async for message in client.messages:
                    await self._handle_message(message)
                    
        except asyncio.CancelledError:
            logger.info("MQTT subscriber stopped")
        except Exception as e:
            logger.error(f"MQTT subscriber error: {e}")
            raise
    
    async def _handle_message(self, message: aiomqtt.Message) -> None:
        """Handle incoming MQTT message"""
        topic = str(message.topic)
        
        try:
            payload = json.loads(message.payload.decode())
        except json.JSONDecodeError:
            payload = {"raw": message.payload.decode()}
        
        logger.debug(f"Received message on {topic}")
        
        # Find matching callbacks
        for pattern, callbacks in self._callbacks.items():
            if self._topic_matches(pattern, topic):
                for callback in callbacks:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(topic, payload)
                        else:
                            callback(topic, payload)
                    except Exception as e:
                        logger.error(f"Callback error for {topic}: {e}")
    
    def _topic_matches(self, pattern: str, topic: str) -> bool:
        """Check if topic matches pattern (supports + and # wildcards)"""
        pattern_parts = pattern.split('/')
        topic_parts = topic.split('/')
        
        i = 0
        for p in pattern_parts:
            if p == '#':
                return True
            if i >= len(topic_parts):
                return False
            if p != '+' and p != topic_parts[i]:
                return False
            i += 1
        
        return i == len(topic_parts)
    
    def stop(self) -> None:
        """Stop the subscriber"""
        self._running = False

