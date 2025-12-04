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

