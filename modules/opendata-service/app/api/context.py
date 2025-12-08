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
JSON-LD Context API
Provides @context definitions for Linked Data
"""
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/context", tags=["JSON-LD Context"])


@router.get("")
async def get_context() -> Dict[str, Any]:
    """
    Get JSON-LD context for GreenEduMap
    
    Returns full @context for mapping terms to URIs
    """
    context = {
        "@context": {
            "@vocab": "http://greenedumap.vn/ontology#",
            "schema": "https://schema.org/",
            "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
            "dcterms": "http://purl.org/dc/terms/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            
            # Entity Types
            "School": "schema:EducationalOrganization",
            "GreenZone": "schema:Park",
            "AirQualityObserved": "https://uri.fiware.org/ns/data-models#AirQualityObserved",
            "GreenCourse": "schema:Course",
            
            # Properties
            "name": "schema:name",
            "description": "schema:description",
            "address": "schema:address",
            "telephone": "schema:telephone",
            "email": "schema:email",
            "url": "schema:url",
            
            # Geo Properties
            "location": {
                "@id": "schema:geo",
                "@type": "schema:GeoCoordinates"
            },
            "latitude": {
                "@id": "geo:lat",
                "@type": "xsd:decimal"
            },
            "longitude": {
                "@id": "geo:long",
                "@type": "xsd:decimal"
            },
            
            # Green Score
            "greenScore": {
                "@id": "http://greenedumap.vn/ontology#greenScore",
                "@type": "xsd:decimal"
            },
            
            # Air Quality Properties
            "aqi": {
                "@id": "http://greenedumap.vn/ontology#aqi",
                "@type": "xsd:integer"
            },
            "pm25": {
                "@id": "http://greenedumap.vn/ontology#pm25",
                "@type": "xsd:decimal"
            },
            "pm10": {
                "@id": "http://greenedumap.vn/ontology#pm10",
                "@type": "xsd:decimal"
            },
            "co": {
                "@id": "http://greenedumap.vn/ontology#co",
                "@type": "xsd:decimal"
            },
            "no2": {
                "@id": "http://greenedumap.vn/ontology#no2",
                "@type": "xsd:decimal"
            },
            "o3": {
                "@id": "http://greenedumap.vn/ontology#o3",
                "@type": "xsd:decimal"
            },
            "so2": {
                "@id": "http://greenedumap.vn/ontology#so2",
                "@type": "xsd:decimal"
            },
            
            # Time
            "dateObserved": {
                "@id": "dcterms:date",
                "@type": "xsd:dateTime"
            },
            "measurementDate": {
                "@id": "dcterms:date",
                "@type": "xsd:dateTime"
            },
            
            # School Properties
            "schoolType": "http://greenedumap.vn/ontology#schoolType",
            "totalStudents": {
                "@id": "http://greenedumap.vn/ontology#totalStudents",
                "@type": "xsd:integer"
            },
            "totalTeachers": {
                "@id": "http://greenedumap.vn/ontology#totalTeachers",
                "@type": "xsd:integer"
            },
            
            # Green Zone Properties
            "zoneType": "http://greenedumap.vn/ontology#zoneType",
            "area": {
                "@id": "http://greenedumap.vn/ontology#areaSqm",
                "@type": "xsd:decimal"
            },
            "amenities": "http://greenedumap.vn/ontology#amenities",
            "openingHours": "schema:openingHours",
            "rating": {
                "@id": "schema:aggregateRating",
                "@type": "xsd:decimal"
            },
            
            # Course Properties
            "course": {
                "@id": "schema:courseCode"
            },
            "category": "schema:category",
            "durationWeeks": {
                "@id": "http://greenedumap.vn/ontology#durationWeeks",
                "@type": "xsd:integer"
            },
            "instructor": "schema:instructor",
            "maxParticipants": {
                "@id": "schema:maximumAttendeeCapacity",
                "@type": "xsd:integer"
            }
        }
    }
    
    return context

