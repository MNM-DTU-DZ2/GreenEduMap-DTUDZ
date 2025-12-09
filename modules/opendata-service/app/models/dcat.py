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

