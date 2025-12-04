"""
CSV Export Service
"""
import csv
import io
from typing import List, Dict, Any


class CSVExporter:
    """Export data to CSV format"""
    
    @staticmethod
    def export_schools(data: List[Dict[str, Any]]) -> str:
        """Export schools to CSV"""
        output = io.StringIO()
        
        if not data:
            return ""
        
        # Define columns
        fieldnames = [
            "id", "name", "code", "address", "city", "district",
            "latitude", "longitude", "green_score",
            "total_students", "total_teachers", "type",
            "created_at", "updated_at"
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def export_air_quality(data: List[Dict[str, Any]]) -> str:
        """Export air quality to CSV"""
        output = io.StringIO()
        
        if not data:
            return ""
        
        fieldnames = [
            "id", "latitude", "longitude", "aqi", "pm25", "pm10",
            "co", "no2", "o3", "so2", "station_name", "station_id",
            "source", "measurement_date", "created_at"
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def export_green_zones(data: List[Dict[str, Any]]) -> str:
        """Export green zones to CSV"""
        output = io.StringIO()
        
        if not data:
            return ""
        
        fieldnames = [
            "id", "name", "zone_type", "description", "latitude", "longitude",
            "area_sqm", "amenities", "opening_hours", "entry_fee", "rating",
            "created_at", "updated_at"
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for row in data:
            # Handle array fields
            if "amenities" in row and isinstance(row["amenities"], list):
                row["amenities"] = "; ".join(row["amenities"])
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def export_green_courses(data: List[Dict[str, Any]]) -> str:
        """Export green courses to CSV"""
        output = io.StringIO()
        
        if not data:
            return ""
        
        fieldnames = [
            "id", "school_id", "title", "description", "category",
            "duration_weeks", "start_date", "end_date",
            "instructor_name", "max_participants", "is_active",
            "created_at", "updated_at"
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)
        
        return output.getvalue()

