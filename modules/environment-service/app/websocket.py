#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

"""
WebSocket endpoints for real-time data streaming
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Set
import asyncio
import logging
from sqlalchemy import text
from shared.database.base import get_session

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"✅ WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"❌ WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


# Global connection managers
aqi_manager = ConnectionManager()
weather_manager = ConnectionManager()


async def get_latest_aqi_data():
    """Fetch latest AQI data from database"""
    async for session in get_session():
        try:
            query = text("""
                SELECT 
                    id, station_name, latitude, longitude,
                    aqi, pm25, pm10, co, no2, o3, so2,
                    source, measurement_date, created_at
                FROM air_quality
                WHERE is_public = true
                ORDER BY created_at DESC
                LIMIT 100
            """)
            
            result = await session.execute(query)
            rows = result.fetchall()
            
            data = [
                {
                    "id": row.id,
                    "station_name": row.station_name,
                    "latitude": float(row.latitude) if row.latitude else None,
                    "longitude": float(row.longitude) if row.longitude else None,
                    "aqi": float(row.aqi) if row.aqi else None,
                    "pm25": float(row.pm25) if row.pm25 else None,
                    "pm10": float(row.pm10) if row.pm10 else None,
                    "co": float(row.co) if row.co else None,
                    "no2": float(row.no2) if row.no2 else None,
                    "o3": float(row.o3) if row.o3 else None,
                    "so2": float(row.so2) if row.so2 else None,
                    "source": row.source,
                    "measurement_date": row.measurement_date.isoformat() if row.measurement_date else None,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                }
                for row in rows
            ]
            
            return data
        except Exception as e:
            logger.error(f"Error fetching AQI data: {e}")
            return []


async def get_latest_weather_data():
    """Fetch latest weather data from database"""
    async for session in get_session():
        try:
            query = text("""
                SELECT 
                    id, city_name, latitude, longitude,
                    temperature, feels_like, humidity, pressure,
                    wind_speed, wind_direction, cloudiness,
                    description, icon, source, measurement_date, created_at
                FROM weather
                WHERE is_public = true
                ORDER BY created_at DESC
                LIMIT 100
            """)
            
            result = await session.execute(query)
            rows = result.fetchall()
            
            data = [
                {
                    "id": row.id,
                    "city_name": row.city_name,
                    "latitude": float(row.latitude) if row.latitude else None,
                    "longitude": float(row.longitude) if row.longitude else None,
                    "temperature": float(row.temperature) if row.temperature else None,
                    "feels_like": float(row.feels_like) if row.feels_like else None,
                    "humidity": float(row.humidity) if row.humidity else None,
                    "pressure": float(row.pressure) if row.pressure else None,
                    "wind_speed": float(row.wind_speed) if row.wind_speed else None,
                    "wind_direction": float(row.wind_direction) if row.wind_direction else None,
                    "cloudiness": float(row.cloudiness) if row.cloudiness else None,
                    "description": row.description,
                    "icon": row.icon,
                    "source": row.source,
                    "measurement_date": row.measurement_date.isoformat() if row.measurement_date else None,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                }
                for row in rows
            ]
            
            return data
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return []


async def aqi_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time AQI data"""
    await aqi_manager.connect(websocket)
    
    try:
        # Send initial data
        data = await get_latest_aqi_data()
        await websocket.send_json({
            "type": "initial",
            "data": data,
            "count": len(data)
        })
        
        # Keep connection alive and send updates every 3 minutes
        while True:
            await asyncio.sleep(180)  # 3 minutes
            
            data = await get_latest_aqi_data()
            await websocket.send_json({
                "type": "update",
                "data": data,
                "count": len(data)
            })
            logger.info(f"📊 Sent AQI update: {len(data)} points")
            
    except WebSocketDisconnect:
        aqi_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        aqi_manager.disconnect(websocket)


async def weather_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time weather data"""
    await weather_manager.connect(websocket)
    
    try:
        # Send initial data
        data = await get_latest_weather_data()
        await websocket.send_json({
            "type": "initial",
            "data": data,
            "count": len(data)
        })
        
        # Keep connection alive and send updates every 3 minutes
        while True:
            await asyncio.sleep(180)  # 3 minutes
            
            data = await get_latest_weather_data()
            await websocket.send_json({
                "type": "update",
                "data": data,
                "count": len(data)
            })
            logger.info(f"🌡️ Sent weather update: {len(data)} points")
            
    except WebSocketDisconnect:
        weather_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        weather_manager.disconnect(websocket)
