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
Transform database entities to NGSI-LD format
"""
from typing import Dict, Any, Optional
from datetime import datetime
from app.models.ngsi_ld import (
    NGSILDProperty, NGSILDGeoProperty,
    AirQualityObservedNGSILD, SchoolNGSILD, GreenZoneNGSILD, GreenCourseNGSILD, NGSILDRelationship
)
from app.utils.vocabularies import get_entity_uri


class EntityTransformer:
    """Transform DB entities to NGSI-LD"""
    
    @staticmethod
    def db_to_ngsi_ld(entity_type: str, db_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform database record to NGSI-LD entity
        
        Args:
            entity_type: Type of entity (air_quality, school, green_zone, etc.)
            db_data: Raw database record
            
        Returns:
            NGSI-LD formatted entity
        """
        if entity_type == "air_quality":
            return EntityTransformer._air_quality_to_ngsi_ld(db_data)
        elif entity_type == "school":
            return EntityTransformer._school_to_ngsi_ld(db_data)
        elif entity_type == "green_zone":
            return EntityTransformer._green_zone_to_ngsi_ld(db_data)
        elif entity_type == "green_course":
            return EntityTransformer._green_course_to_ngsi_ld(db_data)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
    
    @staticmethod
    def _air_quality_to_ngsi_ld(db_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform air quality data to NGSI-LD"""
        entity_id = get_entity_uri("AirQualityObserved", str(db_data["id"]))
        
        # Extract location (PostGIS)
        lat = db_data.get("latitude", 0)
        lon = db_data.get("longitude", 0)
        
        entity = AirQualityObservedNGSILD(
            id=entity_id,
            context=[
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "https://raw.githubusercontent.com/smart-data-models/dataModel.Environment/master/context.jsonld"
            ]
        )
        
        # Add properties
        if db_data.get("aqi") is not None:
            entity.aqi = NGSILDProperty(value=float(db_data["aqi"]), unitCode="AQI")
        
        if db_data.get("pm25") is not None:
            entity.pm25 = NGSILDProperty(value=float(db_data["pm25"]), unitCode="GQ")
        
        if db_data.get("pm10") is not None:
            entity.pm10 = NGSILDProperty(value=float(db_data["pm10"]), unitCode="GQ")
        
        if db_data.get("co") is not None:
            entity.co = NGSILDProperty(value=float(db_data["co"]), unitCode="GP")
        
        if db_data.get("no2") is not None:
            entity.no2 = NGSILDProperty(value=float(db_data["no2"]), unitCode="GQ")
        
        if db_data.get("o3") is not None:
            entity.o3 = NGSILDProperty(value=float(db_data["o3"]), unitCode="GQ")
        
        if db_data.get("so2") is not None:
            entity.so2 = NGSILDProperty(value=float(db_data["so2"]), unitCode="GQ")
        
        # Location (GeoJSON Point)
        entity.location = NGSILDGeoProperty(
            value={
                "type": "Point",
                "coordinates": [lon, lat]
            }
        )
        
        if db_data.get("station_name"):
            entity.stationName = NGSILDProperty(value=db_data["station_name"])
        
        if db_data.get("measurement_date"):
            entity.dateObserved = NGSILDProperty(value=db_data["measurement_date"].isoformat())
        
        if db_data.get("source"):
            entity.source = NGSILDProperty(value=db_data["source"])
        
        return entity.model_dump(exclude_none=True, by_alias=True)
    
    @staticmethod
    def _school_to_ngsi_ld(db_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform school data to NGSI-LD"""
        entity_id = get_entity_uri("School", str(db_data["id"]))
        
        lat = db_data.get("latitude", 0)
        lon = db_data.get("longitude", 0)
        
        entity = SchoolNGSILD(
            id=entity_id,
            context=[
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "http://greenedumap.vn/context.jsonld"
            ]
        )
        
        if db_data.get("name"):
            entity.name = NGSILDProperty(value=db_data["name"])
        
        if db_data.get("code"):
            entity.code = NGSILDProperty(value=db_data["code"])
        
        if db_data.get("address"):
            entity.address = NGSILDProperty(value=db_data["address"])
        
        entity.location = NGSILDGeoProperty(
            value={
                "type": "Point",
                "coordinates": [lon, lat]
            }
        )
        
        if db_data.get("green_score") is not None:
            entity.greenScore = NGSILDProperty(value=float(db_data["green_score"]), unitCode="C62")
        
        if db_data.get("total_students") is not None:
            entity.totalStudents = NGSILDProperty(value=int(db_data["total_students"]))
        
        if db_data.get("total_teachers") is not None:
            entity.totalTeachers = NGSILDProperty(value=int(db_data["total_teachers"]))
        
        if db_data.get("type"):
            entity.schoolType = NGSILDProperty(value=db_data["type"])
        
        if db_data.get("city"):
            entity.city = NGSILDProperty(value=db_data["city"])
        
        if db_data.get("district"):
            entity.district = NGSILDProperty(value=db_data["district"])
        
        return entity.model_dump(exclude_none=True, by_alias=True)
    
    @staticmethod
    def _green_zone_to_ngsi_ld(db_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform green zone data to NGSI-LD"""
        entity_id = get_entity_uri("GreenZone", str(db_data["id"]))
        
        lat = db_data.get("latitude", 0)
        lon = db_data.get("longitude", 0)
        
        entity = GreenZoneNGSILD(
            id=entity_id,
            context=[
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "http://greenedumap.vn/context.jsonld"
            ]
        )
        
        if db_data.get("name"):
            entity.name = NGSILDProperty(value=db_data["name"])
        
        if db_data.get("description"):
            entity.description = NGSILDProperty(value=db_data["description"])
        
        if db_data.get("zone_type"):
            entity.zoneType = NGSILDProperty(value=db_data["zone_type"])
        
        entity.location = NGSILDGeoProperty(
            value={
                "type": "Point",
                "coordinates": [lon, lat]
            }
        )
        
        if db_data.get("area_sqm") is not None:
            entity.area = NGSILDProperty(value=float(db_data["area_sqm"]), unitCode="MTK")
        
        if db_data.get("amenities"):
            entity.amenities = NGSILDProperty(value=db_data["amenities"])
        
        if db_data.get("opening_hours"):
            entity.openingHours = NGSILDProperty(value=db_data["opening_hours"])
        
        if db_data.get("rating") is not None:
            entity.rating = NGSILDProperty(value=float(db_data["rating"]))
        
        return entity.model_dump(exclude_none=True, by_alias=True)
    
    @staticmethod
    def _green_course_to_ngsi_ld(db_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform green course data to NGSI-LD"""
        entity_id = get_entity_uri("GreenCourse", str(db_data["id"]))
        
        entity = GreenCourseNGSILD(
            id=entity_id,
            context=[
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
                "http://greenedumap.vn/context.jsonld"
            ]
        )
        
        if db_data.get("title"):
            entity.title = NGSILDProperty(value=db_data["title"])
        
        if db_data.get("description"):
            entity.description = NGSILDProperty(value=db_data["description"])
        
        if db_data.get("category"):
            entity.category = NGSILDProperty(value=db_data["category"])
        
        if db_data.get("duration_weeks") is not None:
            entity.durationWeeks = NGSILDProperty(value=int(db_data["duration_weeks"]), unitCode="WEE")
        
        if db_data.get("start_date"):
            entity.startDate = NGSILDProperty(value=db_data["start_date"].isoformat())
        
        if db_data.get("end_date"):
            entity.endDate = NGSILDProperty(value=db_data["end_date"].isoformat())
        
        if db_data.get("instructor_name"):
            entity.instructor = NGSILDProperty(value=db_data["instructor_name"])
        
        if db_data.get("max_participants") is not None:
            entity.maxParticipants = NGSILDProperty(value=int(db_data["max_participants"]))
        
        # Relationship to School
        if db_data.get("school_id"):
            entity.school = NGSILDRelationship(
                object=get_entity_uri("School", str(db_data["school_id"]))
            )
        
        return entity.model_dump(exclude_none=True, by_alias=True)

