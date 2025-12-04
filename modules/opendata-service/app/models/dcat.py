"""
DCAT-AP (Data Catalog Vocabulary - Application Profile) Models
"""
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class DCATDistribution(BaseModel):
    """DCAT Distribution - represents a specific format of a dataset"""
    id: str
    title: str
    description: Optional[str] = None
    format: str  # CSV, GeoJSON, RDF, JSON-LD
    mediaType: str  # MIME type
    accessURL: HttpUrl
    downloadURL: Optional[HttpUrl] = None
    byteSize: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "schools-csv",
                "title": "Schools Dataset (CSV)",
                "format": "CSV",
                "mediaType": "text/csv",
                "accessURL": "http://localhost:8009/api/v1/export/csv/schools"
            }
        }


class DCATDataset(BaseModel):
    """DCAT Dataset - represents a dataset"""
    id: str
    title: str
    description: str
    keyword: List[str] = []
    theme: List[str] = []
    issued: datetime
    modified: datetime
    publisher: str = "GreenEduMap"
    contactPoint: str = "admin@greenedumap.vn"
    license: str = "https://creativecommons.org/licenses/by/4.0/"
    spatial: Optional[str] = "Vietnam"
    temporal: Optional[str] = None
    distributions: List[DCATDistribution] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "schools",
                "title": "Green Schools Dataset",
                "description": "Schools with environmental scores",
                "keyword": ["education", "green", "schools"],
                "theme": ["environment", "education"],
                "issued": "2025-12-04T00:00:00Z",
                "modified": "2025-12-04T00:00:00Z",
                "publisher": "GreenEduMap",
                "license": "CC-BY-4.0"
            }
        }


class DCATCatalog(BaseModel):
    """DCAT Catalog - represents the entire data catalog"""
    id: str
    title: str
    description: str
    publisher: str = "GreenEduMap"
    homepage: HttpUrl
    language: str = "vi"
    issued: datetime
    modified: datetime
    datasets: List[DCATDataset] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "greenedumap-catalog",
                "title": "GreenEduMap Data Catalog",
                "description": "Open data for environmental education",
                "publisher": "GreenEduMap",
                "homepage": "http://greenedumap.vn",
                "language": "vi"
            }
        }

