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
Data Ingestion Service for GreenEduMap
Fetches real-time weather and air quality data from OpenWeatherMap API
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Dict
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "14beef0ff70a6296493bea7c2ef80cf8")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgres:5432/greenedumap")
UPDATE_INTERVAL_MINUTES = int(os.getenv("UPDATE_INTERVAL_MINUTES", "3"))

# Location strategy: 'database', 'vietnam_grid', or 'static'
LOCATION_STRATEGY = os.getenv("LOCATION_STRATEGY", "database")

# Static locations (fallback)
STATIC_LOCATIONS = [
    {"name": "Da Nang Center", "lat": 16.0678, "lon": 108.2208},
    {"name": "Son Tra", "lat": 16.1063, "lon": 108.2651},
    {"name": "Hai Chau", "lat": 16.0544, "lon": 108.2022},
    {"name": "Thanh Khe", "lat": 16.0734, "lon": 108.1881},
    {"name": "Ngu Hanh Son", "lat": 16.0007, "lon": 108.2626},
]

# Database engine
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def generate_vietnam_grid(spacing_degrees=1.0):
    """
    Generate grid of locations covering Vietnam
    
    Args:
        spacing_degrees: Distance between points in degrees (1.0 ≈ 111km)
    
    Returns:
        List of location dicts
    """
    locations = []
    
    # Vietnam boundaries (approximate)
    lat_min, lat_max = 8.5, 23.4   # South to North
    lon_min, lon_max = 102.1, 109.5  # West to East
    
    # Major cities (always include)
    major_cities = [
        {"name": "Hà Nội", "lat": 21.0285, "lon": 105.8542},
        {"name": "TP.HCM", "lat": 10.8231, "lon": 106.6297},
        {"name": "Đà Nẵng", "lat": 16.0678, "lon": 108.2208},
        {"name": "Hải Phòng", "lat": 20.8449, "lon": 106.6881},
        {"name": "Cần Thơ", "lat": 10.0452, "lon": 105.7469},
    ]
    locations.extend(major_cities)
    
    # Grid coverage
    lat = lat_min
    while lat <= lat_max:
        lon = lon_min
        while lon <= lon_max:
            # Skip if too close to major cities
            too_close = any(
                abs(city["lat"] - lat) < 0.5 and abs(city["lon"] - lon) < 0.5
                for city in major_cities
            )
            if not too_close:
                locations.append({
                    "name": f"Grid_{lat:.1f}_{lon:.1f}",
                    "lat": round(lat, 2),
                    "lon": round(lon, 2)
                })
            lon += spacing_degrees
        lat += spacing_degrees
    
    logger.info(f"📍 Generated Vietnam grid: {len(locations)} locations")
    return locations


async def get_locations_from_database(max_locations=50):
    """
    Get locations from database (schools + green zones)
    
    Args:
        max_locations: Maximum number of locations to fetch
    
    Returns:
        List of location dicts
    """
    async with async_session() as session:
        try:
            # Get from schools
            query = text("""
                SELECT 
                    name,
                    ST_Y(location::geometry) as lat,
                    ST_X(location::geometry) as lon
                FROM schools
                WHERE location IS NOT NULL
                ORDER BY created_at DESC
                LIMIT :limit
            """)
            
            result = await session.execute(query, {"limit": max_locations // 2})
            schools = result.fetchall()
            
            # Get from green zones
            query = text("""
                SELECT 
                    name,
                    ST_Y(location::geometry) as lat,
                    ST_X(location::geometry) as lon
                FROM green_zones
                WHERE location IS NOT NULL
                ORDER BY created_at DESC
                LIMIT :limit
            """)
            
            result = await session.execute(query, {"limit": max_locations // 2})
            zones = result.fetchall()
            
            # Combine and deduplicate
            locations = []
            seen = set()
            
            for row in list(schools) + list(zones):
                # Round to 2 decimals to avoid duplicates
                lat_lon = (round(float(row.lat), 2), round(float(row.lon), 2))
                if lat_lon not in seen:
                    seen.add(lat_lon)
                    locations.append({
                        "name": row.name,
                        "lat": float(row.lat),
                        "lon": float(row.lon)
                    })
            
            logger.info(f"📍 Fetched {len(locations)} locations from database")
            return locations
            
        except Exception as e:
            logger.error(f"Error fetching locations from database: {e}")
            logger.info("📍 Falling back to static locations")
            return STATIC_LOCATIONS


async def get_locations():
    """
    Get locations based on strategy
    
    Returns:
        List of location dicts
    """
    if LOCATION_STRATEGY == "vietnam_grid":
        # Grid coverage for entire Vietnam (spacing = 1 degree ≈ 111km)
        return generate_vietnam_grid(spacing_degrees=1.0)
    
    elif LOCATION_STRATEGY == "database":
        # Dynamic from database
        return await get_locations_from_database(max_locations=50)
    
    else:
        # Static locations
        logger.info("📍 Using static locations")
        return STATIC_LOCATIONS


class OpenWeatherFetcher:
    """Fetches data from OpenWeatherMap API"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def fetch_current_weather(self, lat: float, lon: float) -> Dict:
        """Fetch current weather for location"""
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/weather",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching weather for ({lat}, {lon}): {e}")
            return None
    
    async def fetch_air_quality(self, lat: float, lon: float) -> Dict:
        """Fetch air quality for location"""
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/air_pollution",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching AQI for ({lat}, {lon}): {e}")
            return None
    
    async def close(self):
        await self.client.aclose()


async def save_weather_data(session: AsyncSession, location: Dict, weather_data: Dict):
    """Save weather data to database"""
    if not weather_data:
        return
    
    try:
        query = text("""
            INSERT INTO weather (
                city_name, location, temperature, feels_like,
                humidity, pressure, wind_speed, wind_direction, clouds,
                weather_description, weather_icon, source, observation_time, is_public
            ) VALUES (
                :city_name, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                :temperature, :feels_like, :humidity, :pressure, :wind_speed,
                :wind_direction, :cloudiness, :description, :icon, :source, :measurement_date, true
            )
        """)
        
        await session.execute(query, {
            "city_name": location["name"],
            "lat": location["lat"],
            "lon": location["lon"],
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "wind_speed": weather_data["wind"]["speed"],
            "wind_direction": weather_data["wind"].get("deg", 0),
            "cloudiness": weather_data["clouds"]["all"],
            "description": weather_data["weather"][0]["description"],
            "icon": weather_data["weather"][0]["icon"],
            "source": "OpenWeatherMap",
            "measurement_date": datetime.fromtimestamp(weather_data["dt"])
        })
        
        await session.commit()
        logger.info(f"✅ Saved weather data for {location['name']}")
    except Exception as e:
        logger.error(f"Error saving weather data: {e}")
        await session.rollback()


async def save_aqi_data(session: AsyncSession, location: Dict, aqi_data: Dict):
    """Save air quality data to database"""
    if not aqi_data or "list" not in aqi_data or len(aqi_data["list"]) == 0:
        return
    
    try:
        data = aqi_data["list"][0]
        components = data["components"]
        
        # Calculate AQI from components (simplified)
        pm25 = components.get("pm2_5", 0)
        aqi = min(int(pm25 * 2), 500)  # Simplified AQI calculation
        
        query = text("""
            INSERT INTO air_quality (
                station_name, location, aqi, pm25, pm10,
                co, no2, o3, so2, source, measurement_date, is_public
            ) VALUES (
                :station_name, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
                :aqi, :pm25, :pm10, :co, :no2, :o3, :so2, :source, :measurement_date, true
            )
        """)
        
        await session.execute(query, {
            "station_name": location["name"],
            "lat": location["lat"],
            "lon": location["lon"],
            "aqi": aqi,
            "pm25": components.get("pm2_5"),
            "pm10": components.get("pm10"),
            "co": components.get("co"),
            "no2": components.get("no2"),
            "o3": components.get("o3"),
            "so2": components.get("so2"),
            "source": "OpenWeatherMap",
            "measurement_date": datetime.fromtimestamp(data["dt"])
        })
        
        await session.commit()
        logger.info(f"✅ Saved AQI data for {location['name']} (AQI: {aqi})")
    except Exception as e:
        logger.error(f"Error saving AQI data: {e}")
        await session.rollback()


async def fetch_and_save_all_data():
    """Fetch and save data for all locations"""
    logger.info("🔄 Starting data fetch cycle...")
    
    # Get locations based on strategy
    locations = await get_locations()
    
    fetcher = OpenWeatherFetcher(OPENWEATHER_API_KEY)
    
    async with async_session() as session:
        for location in locations:
            # Fetch weather
            weather_data = await fetcher.fetch_current_weather(location["lat"], location["lon"])
            if weather_data:
                await save_weather_data(session, location, weather_data)
            
            # Fetch air quality
            aqi_data = await fetcher.fetch_air_quality(location["lat"], location["lon"])
            if aqi_data:
                await save_aqi_data(session, location, aqi_data)
            
            # Small delay between requests
            await asyncio.sleep(0.5)
    
    await fetcher.close()
    logger.info(f"✅ Data fetch cycle completed at {datetime.now()}")


async def main():
    """Main function to run the scheduler"""
    logger.info("🚀 Starting Data Ingestion Service")
    logger.info(f"📡 OpenWeatherMap API Key: {OPENWEATHER_API_KEY[:10]}...")
    logger.info(f"⏱️  Update interval: {UPDATE_INTERVAL_MINUTES} minutes")
    logger.info(f"📍 Location strategy: {LOCATION_STRATEGY}")
    
    # Get initial locations
    locations = await get_locations()
    logger.info(f"📍 Monitoring {len(locations)} locations")
    
    # Create scheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule job to run every N minutes
    scheduler.add_job(
        fetch_and_save_all_data,
        'interval',
        minutes=UPDATE_INTERVAL_MINUTES,
        id='fetch_data',
        name='Fetch Weather and AQI Data',
        replace_existing=True
    )
    
    # Start scheduler
    scheduler.start()
    logger.info(f"✅ Scheduler started - will fetch data every {UPDATE_INTERVAL_MINUTES} minutes")
    
    # Run first fetch immediately
    await fetch_and_save_all_data()
    
    # Keep the script running
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Shutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
