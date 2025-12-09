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
NGSI-LD Entity Models
Following ETSI GS CIM 009 specification
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class NGSILDProperty(BaseModel):
    """NGSI-LD Property"""
    type: str = "Property"
    value: Any
    observedAt: Optional[datetime] = None
    unitCode: Optional[str] = None


class NGSILDGeoProperty(BaseModel):
    """NGSI-LD GeoProperty"""
    type: str = "GeoProperty"
    value: Dict[str, Any]  # GeoJSON geometry


class NGSILDRelationship(BaseModel):
    """NGSI-LD Relationship"""
    type: str = "Relationship"
    object: str  # URI of related entity


class NGSILDEntity(BaseModel):
    """Base NGSI-LD Entity"""
    id: str  # URI
    type: str  # Entity type URI
    context: List[str] = Field(default=["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"], alias="@context")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "urn:ngsi-ld:AirQualityObserved:danang-001",
                "type": "AirQualityObserved",
                "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]
            }
        }


# Specific Entity Types

class AirQualityObservedNGSILD(NGSILDEntity):
    """NGSI-LD AirQualityObserved Entity"""
    type: str = "AirQualityObserved"
    aqi: Optional[NGSILDProperty] = None
    pm25: Optional[NGSILDProperty] = None
    pm10: Optional[NGSILDProperty] = None
    co: Optional[NGSILDProperty] = None
    no2: Optional[NGSILDProperty] = None
    o3: Optional[NGSILDProperty] = None
    so2: Optional[NGSILDProperty] = None
    location: Optional[NGSILDGeoProperty] = None
    address: Optional[NGSILDProperty] = None
    stationName: Optional[NGSILDProperty] = None
    dateObserved: Optional[NGSILDProperty] = None
    source: Optional[NGSILDProperty] = None


class SchoolNGSILD(NGSILDEntity):
    """NGSI-LD School Entity"""
    type: str = "School"
    name: Optional[NGSILDProperty] = None
    code: Optional[NGSILDProperty] = None
    address: Optional[NGSILDProperty] = None
    location: Optional[NGSILDGeoProperty] = None
    greenScore: Optional[NGSILDProperty] = None
    totalStudents: Optional[NGSILDProperty] = None
    totalTeachers: Optional[NGSILDProperty] = None
    schoolType: Optional[NGSILDProperty] = None
    city: Optional[NGSILDProperty] = None
    district: Optional[NGSILDProperty] = None


class GreenZoneNGSILD(NGSILDEntity):
    """NGSI-LD GreenZone Entity"""
    type: str = "GreenZone"
    name: Optional[NGSILDProperty] = None
    description: Optional[NGSILDProperty] = None
    zoneType: Optional[NGSILDProperty] = None
    location: Optional[NGSILDGeoProperty] = None
    area: Optional[NGSILDProperty] = None
    amenities: Optional[NGSILDProperty] = None
    openingHours: Optional[NGSILDProperty] = None
    rating: Optional[NGSILDProperty] = None


class GreenCourseNGSILD(NGSILDEntity):
    """NGSI-LD GreenCourse Entity"""
    type: str = "GreenCourse"
    title: Optional[NGSILDProperty] = None
    description: Optional[NGSILDProperty] = None
    category: Optional[NGSILDProperty] = None
    durationWeeks: Optional[NGSILDProperty] = None
    startDate: Optional[NGSILDProperty] = None
    endDate: Optional[NGSILDProperty] = None
    instructor: Optional[NGSILDProperty] = None
    maxParticipants: Optional[NGSILDProperty] = None
    school: Optional[NGSILDRelationship] = None  # Relationship to School

