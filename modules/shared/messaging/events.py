"""
Event definitions and utilities for GreenEduMap messaging
"""
import json
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict
import uuid


class EventTypes(str, Enum):
    """Standard event types for GreenEduMap"""
    
    # Environment Events
    AIR_QUALITY_UPDATED = "air_quality.updated"
    AIR_QUALITY_ALERT = "air_quality.alert"
    WEATHER_UPDATED = "weather.updated"
    WEATHER_ALERT = "weather.alert"
    SENSOR_DATA_RECEIVED = "sensor.data_received"
    
    # Education Events
    SCHOOL_CREATED = "school.created"
    SCHOOL_UPDATED = "school.updated"
    SCHOOL_DELETED = "school.deleted"
    GREEN_SCORE_UPDATED = "school.green_score_updated"
    COURSE_CREATED = "course.created"
    COURSE_UPDATED = "course.updated"
    ENROLLMENT_CREATED = "enrollment.created"
    
    # AI Events
    AI_CLUSTERING_REQUESTED = "ai.clustering.requested"
    AI_CLUSTERING_COMPLETED = "ai.clustering.completed"
    AI_PREDICTION_REQUESTED = "ai.prediction.requested"
    AI_PREDICTION_COMPLETED = "ai.prediction.completed"
    AI_CORRELATION_REQUESTED = "ai.correlation.requested"
    AI_CORRELATION_COMPLETED = "ai.correlation.completed"
    
    # Export Events
    EXPORT_REQUESTED = "export.requested"
    EXPORT_COMPLETED = "export.completed"
    EXPORT_FAILED = "export.failed"
    
    # System Events
    SERVICE_STARTED = "system.service_started"
    SERVICE_STOPPED = "system.service_stopped"
    ERROR_OCCURRED = "system.error"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class Event:
    """Base event structure"""
    event_id: str
    event_type: str
    timestamp: str
    source: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "Event":
        return cls.from_dict(json.loads(json_str))


def create_event(
    event_type: EventTypes | str,
    source: str,
    data: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> Event:
    """Create a standardized event"""
    return Event(
        event_id=str(uuid.uuid4()),
        event_type=event_type.value if isinstance(event_type, EventTypes) else event_type,
        timestamp=datetime.utcnow().isoformat() + "Z",
        source=source,
        data=data,
        metadata=metadata or {}
    )


def parse_event(message: Dict[str, Any] | str) -> Event:
    """Parse a message into an Event"""
    if isinstance(message, str):
        return Event.from_json(message)
    return Event.from_dict(message)


# Sensor data schemas
@dataclass
class AirQualitySensorData:
    """Air quality sensor data structure"""
    location_id: str
    latitude: float
    longitude: float
    aqi: float
    pm25: float
    pm10: Optional[float] = None
    co: Optional[float] = None
    no2: Optional[float] = None
    o3: Optional[float] = None
    so2: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass  
class WeatherSensorData:
    """Weather sensor data structure"""
    location_id: str
    latitude: float
    longitude: float
    temperature: float
    humidity: float
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    clouds: Optional[int] = None
    visibility: Optional[int] = None
    weather_main: Optional[str] = None
    weather_description: Optional[str] = None
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


# AI Task schemas
@dataclass
class AIClusteringTask:
    """AI clustering task structure"""
    task_id: str
    data_type: str  # "environment", "education", "combined"
    parameters: Dict[str, Any]
    callback_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AICorrelationTask:
    """AI correlation analysis task"""
    task_id: str
    environment_data_ids: list
    education_data_ids: list
    analysis_type: str  # "pearson", "spearman", "regression"
    parameters: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

