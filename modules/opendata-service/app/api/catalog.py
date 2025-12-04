"""
DCAT-AP Catalog API
Data Catalog Vocabulary - Application Profile
"""
from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
from app.models.dcat import DCATCatalog, DCATDataset, DCATDistribution
from app.core.config import settings

router = APIRouter(prefix="/catalog", tags=["DCAT-AP Catalog"])


@router.get("", response_model=DCATCatalog)
async def get_catalog() -> DCATCatalog:
    """
    Get DCAT-AP compliant data catalog
    
    Returns complete catalog with all datasets and distributions
    """
    now = datetime.utcnow()
    
    # Dataset 1: Schools
    schools_dataset = DCATDataset(
        id="schools",
        title="Green Schools Dataset",
        description="Educational institutions in Vietnam with environmental green scores, locations, and student information",
        keyword=["education", "green", "schools", "environment", "sustainability"],
        theme=["environment", "education"],
        issued=datetime(2025, 12, 1),
        modified=now,
        publisher="GreenEduMap",
        contactPoint="data@greenedumap.vn",
        license="https://creativecommons.org/licenses/by/4.0/",
        spatial="Vietnam",
        temporal="2025-present",
        distributions=[
            DCATDistribution(
                id="schools-ngsi-ld",
                title="Schools (NGSI-LD)",
                description="Schools in NGSI-LD format",
                format="JSON-LD",
                mediaType="application/ld+json",
                accessURL=f"{settings.BASE_URL}/api/v1/entities?type=School"
            ),
            DCATDistribution(
                id="schools-csv",
                title="Schools (CSV)",
                description="Schools in CSV format",
                format="CSV",
                mediaType="text/csv",
                accessURL=f"{settings.BASE_URL}/api/v1/export/csv/schools",
                downloadURL=f"{settings.BASE_URL}/api/v1/export/csv/schools"
            ),
            DCATDistribution(
                id="schools-geojson",
                title="Schools (GeoJSON)",
                description="Schools with geographic data in GeoJSON format",
                format="GeoJSON",
                mediaType="application/geo+json",
                accessURL=f"{settings.BASE_URL}/api/v1/export/geojson/schools",
                downloadURL=f"{settings.BASE_URL}/api/v1/export/geojson/schools"
            ),
            DCATDistribution(
                id="schools-rdf",
                title="Schools (RDF Turtle)",
                description="Schools as Linked Data in Turtle format",
                format="TTL",
                mediaType="text/turtle",
                accessURL=f"{settings.BASE_URL}/api/v1/export/rdf/schools?format=turtle",
                downloadURL=f"{settings.BASE_URL}/api/v1/export/rdf/schools?format=turtle"
            )
        ]
    )
    
    # Dataset 2: Air Quality
    air_quality_dataset = DCATDataset(
        id="air-quality",
        title="Air Quality Observations",
        description="Real-time and historical air quality measurements including AQI, PM2.5, PM10, and other pollutants from monitoring stations",
        keyword=["air quality", "AQI", "pollution", "environment", "PM2.5", "sensors"],
        theme=["environment", "health"],
        issued=datetime(2025, 12, 1),
        modified=now,
        publisher="GreenEduMap",
        contactPoint="data@greenedumap.vn",
        license="https://creativecommons.org/licenses/by/4.0/",
        spatial="Vietnam - Da Nang",
        temporal="2025-present",
        distributions=[
            DCATDistribution(
                id="aqi-ngsi-ld",
                title="Air Quality (NGSI-LD)",
                description="Air quality in NGSI-LD format",
                format="JSON-LD",
                mediaType="application/ld+json",
                accessURL=f"{settings.BASE_URL}/api/v1/entities?type=AirQualityObserved"
            ),
            DCATDistribution(
                id="aqi-csv",
                title="Air Quality (CSV)",
                description="Air quality time series in CSV format",
                format="CSV",
                mediaType="text/csv",
                accessURL=f"{settings.BASE_URL}/api/v1/export/csv/air-quality",
                downloadURL=f"{settings.BASE_URL}/api/v1/export/csv/air-quality"
            ),
            DCATDistribution(
                id="aqi-geojson",
                title="Air Quality (GeoJSON)",
                description="Air quality with monitoring station locations",
                format="GeoJSON",
                mediaType="application/geo+json",
                accessURL=f"{settings.BASE_URL}/api/v1/export/geojson/air-quality"
            ),
            DCATDistribution(
                id="aqi-rdf",
                title="Air Quality (RDF Turtle)",
                description="Air quality as Linked Data",
                format="TTL",
                mediaType="text/turtle",
                accessURL=f"{settings.BASE_URL}/api/v1/export/rdf/air-quality?format=turtle"
            )
        ]
    )
    
    # Dataset 3: Green Zones
    green_zones_dataset = DCATDataset(
        id="green-zones",
        title="Green Zones Dataset",
        description="Parks, forests, gardens, and other green spaces with location, area, amenities, and ratings",
        keyword=["parks", "green spaces", "forests", "recreation", "environment"],
        theme=["environment", "recreation"],
        issued=datetime(2025, 12, 1),
        modified=now,
        publisher="GreenEduMap",
        contactPoint="data@greenedumap.vn",
        license="https://creativecommons.org/licenses/by/4.0/",
        spatial="Vietnam",
        distributions=[
            DCATDistribution(
                id="zones-ngsi-ld",
                title="Green Zones (NGSI-LD)",
                format="JSON-LD",
                mediaType="application/ld+json",
                accessURL=f"{settings.BASE_URL}/api/v1/entities?type=GreenZone"
            ),
            DCATDistribution(
                id="zones-csv",
                title="Green Zones (CSV)",
                format="CSV",
                mediaType="text/csv",
                accessURL=f"{settings.BASE_URL}/api/v1/export/csv/green-zones"
            ),
            DCATDistribution(
                id="zones-geojson",
                title="Green Zones (GeoJSON)",
                format="GeoJSON",
                mediaType="application/geo+json",
                accessURL=f"{settings.BASE_URL}/api/v1/export/geojson/green-zones"
            )
        ]
    )
    
    # Dataset 4: Green Courses
    green_courses_dataset = DCATDataset(
        id="green-courses",
        title="Environmental Education Courses",
        description="Green courses offered by educational institutions covering topics like energy, waste, water, and biodiversity",
        keyword=["education", "courses", "environment", "sustainability", "training"],
        theme=["education", "environment"],
        issued=datetime(2025, 12, 1),
        modified=now,
        publisher="GreenEduMap",
        contactPoint="data@greenedumap.vn",
        license="https://creativecommons.org/licenses/by/4.0/",
        spatial="Vietnam",
        distributions=[
            DCATDistribution(
                id="courses-ngsi-ld",
                title="Green Courses (NGSI-LD)",
                format="JSON-LD",
                mediaType="application/ld+json",
                accessURL=f"{settings.BASE_URL}/api/v1/entities?type=GreenCourse"
            ),
            DCATDistribution(
                id="courses-csv",
                title="Green Courses (CSV)",
                format="CSV",
                mediaType="text/csv",
                accessURL=f"{settings.BASE_URL}/api/v1/export/csv/green-courses"
            )
        ]
    )
    
    # Build catalog
    catalog = DCATCatalog(
        id="greenedumap-catalog",
        title="GreenEduMap Open Data Catalog",
        description="Open data portal for environmental education in Vietnam. Provides air quality data, school information, green zones, and educational resources in multiple formats including NGSI-LD, CSV, GeoJSON, and RDF.",
        publisher="GreenEduMap Project",
        homepage=settings.BASE_URL,
        issued=datetime(2025, 12, 1),
        modified=now,
        language="vi",
        datasets=[
            schools_dataset,
            air_quality_dataset,
            green_zones_dataset,
            green_courses_dataset
        ]
    )
    
    return catalog


@router.get("/datasets")
async def list_datasets() -> Dict[str, Any]:
    """
    List all available datasets
    
    Returns summary of datasets with their distributions
    """
    catalog = await get_catalog()
    
    return {
        "total": len(catalog.datasets),
        "datasets": [
            {
                "id": ds.id,
                "title": ds.title,
                "description": ds.description,
                "keyword": ds.keyword,
                "distributions": len(ds.distributions)
            }
            for ds in catalog.datasets
        ]
    }


@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str) -> DCATDataset:
    """
    Get specific dataset by ID
    
    Returns dataset with all distributions
    """
    catalog = await get_catalog()
    
    for dataset in catalog.datasets:
        if dataset.id == dataset_id:
            return dataset
    
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found")

