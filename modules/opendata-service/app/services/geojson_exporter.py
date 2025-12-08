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
GeoJSON Export Service
"""
from typing import List, Dict, Any
import json


class GeoJSONExporter:
    """Export data to GeoJSON format"""
    
    @staticmethod
    def export(data: List[Dict[str, Any]], entity_type: str) -> Dict[str, Any]:
        """
        Export data to GeoJSON FeatureCollection
        
        Args:
            data: List of entities with latitude/longitude
            entity_type: Type of entity (for metadata)
            
        Returns:
            GeoJSON FeatureCollection
        """
        features = []
        
        for item in data:
            lat = item.get("latitude", 0)
            lon = item.get("longitude", 0)
            
            # Create properties (exclude lat/lon)
            properties = {k: v for k, v in item.items() if k not in ["latitude", "longitude"]}
            
            # Convert datetime to ISO string
            for key, value in properties.items():
                if hasattr(value, 'isoformat'):
                    properties[key] = value.isoformat()
            
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": properties
            }
            
            features.append(feature)
        
        geojson = {
            "type": "FeatureCollection",
            "metadata": {
                "count": len(features),
                "entity_type": entity_type,
                "crs": "EPSG:4326"
            },
            "features": features
        }
        
        return geojson
    
    @staticmethod
    def to_string(geojson: Dict[str, Any]) -> str:
        """Convert GeoJSON to formatted string"""
        return json.dumps(geojson, indent=2, ensure_ascii=False)

