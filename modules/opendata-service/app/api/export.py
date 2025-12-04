"""
Export API - CSV, GeoJSON, RDF
Multiple format exports for Open Data
"""
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.api.entities import (
    load_air_quality_data,
    load_schools_data,
    load_green_zones_data,
    load_green_courses_data
)
from app.services.csv_exporter import CSVExporter
from app.services.geojson_exporter import GeoJSONExporter
from app.services.rdf_exporter import RDFExporter

router = APIRouter(prefix="/export", tags=["Export"])


# ========== CSV EXPORTS ==========

@router.get("/csv/schools")
async def export_schools_csv(
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export schools to CSV"""
    data = await load_schools_data(db, limit)
    csv_content = CSVExporter.export_schools(data)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=schools.csv"}
    )


@router.get("/csv/air-quality")
async def export_air_quality_csv(
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export air quality to CSV"""
    data = await load_air_quality_data(db, limit)
    csv_content = CSVExporter.export_air_quality(data)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=air_quality.csv"}
    )


@router.get("/csv/green-zones")
async def export_green_zones_csv(
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export green zones to CSV"""
    data = await load_green_zones_data(db, limit)
    csv_content = CSVExporter.export_green_zones(data)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=green_zones.csv"}
    )


@router.get("/csv/green-courses")
async def export_green_courses_csv(
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export green courses to CSV"""
    data = await load_green_courses_data(db, limit)
    csv_content = CSVExporter.export_green_courses(data)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=green_courses.csv"}
    )


# ========== GEOJSON EXPORTS ==========

@router.get("/geojson/schools")
async def export_schools_geojson(
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export schools to GeoJSON"""
    data = await load_schools_data(db, limit)
    geojson = GeoJSONExporter.export(data, "schools")
    
    return Response(
        content=GeoJSONExporter.to_string(geojson),
        media_type="application/geo+json",
        headers={"Content-Disposition": "attachment; filename=schools.geojson"}
    )


@router.get("/geojson/air-quality")
async def export_air_quality_geojson(
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export air quality to GeoJSON"""
    data = await load_air_quality_data(db, limit)
    geojson = GeoJSONExporter.export(data, "air_quality")
    
    return Response(
        content=GeoJSONExporter.to_string(geojson),
        media_type="application/geo+json",
        headers={"Content-Disposition": "attachment; filename=air_quality.geojson"}
    )


@router.get("/geojson/green-zones")
async def export_green_zones_geojson(
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export green zones to GeoJSON"""
    data = await load_green_zones_data(db, limit)
    geojson = GeoJSONExporter.export(data, "green_zones")
    
    return Response(
        content=GeoJSONExporter.to_string(geojson),
        media_type="application/geo+json",
        headers={"Content-Disposition": "attachment; filename=green_zones.geojson"}
    )


# ========== RDF EXPORTS ==========

@router.get("/rdf/schools")
async def export_schools_rdf(
    format: str = Query("turtle", regex="^(turtle|ntriples|jsonld|xml)$"),
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export schools to RDF (Turtle/N-Triples/JSON-LD/XML)"""
    data = await load_schools_data(db, limit)
    
    exporter = RDFExporter()
    for school in data:
        exporter.add_school(school)
    
    if format == "turtle":
        content = exporter.export_turtle()
        media_type = "text/turtle"
        ext = "ttl"
    elif format == "ntriples":
        content = exporter.export_ntriples()
        media_type = "application/n-triples"
        ext = "nt"
    elif format == "jsonld":
        content = exporter.export_jsonld()
        media_type = "application/ld+json"
        ext = "jsonld"
    else:  # xml
        content = exporter.export_rdfxml()
        media_type = "application/rdf+xml"
        ext = "rdf"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename=schools.{ext}"}
    )


@router.get("/rdf/air-quality")
async def export_air_quality_rdf(
    format: str = Query("turtle", regex="^(turtle|ntriples|jsonld|xml)$"),
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export air quality to RDF (Turtle/N-Triples/JSON-LD/XML)"""
    data = await load_air_quality_data(db, limit)
    
    exporter = RDFExporter()
    for aqi in data:
        exporter.add_air_quality(aqi)
    
    if format == "turtle":
        content = exporter.export_turtle()
        media_type = "text/turtle"
        ext = "ttl"
    elif format == "ntriples":
        content = exporter.export_ntriples()
        media_type = "application/n-triples"
        ext = "nt"
    elif format == "jsonld":
        content = exporter.export_jsonld()
        media_type = "application/ld+json"
        ext = "jsonld"
    else:  # xml
        content = exporter.export_rdfxml()
        media_type = "application/rdf+xml"
        ext = "rdf"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename=air_quality.{ext}"}
    )


@router.get("/rdf/green-zones")
async def export_green_zones_rdf(
    format: str = Query("turtle", regex="^(turtle|ntriples|jsonld|xml)$"),
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db)
):
    """Export green zones to RDF (Turtle/N-Triples/JSON-LD/XML)"""
    data = await load_green_zones_data(db, limit)
    
    exporter = RDFExporter()
    for zone in data:
        exporter.add_green_zone(zone)
    
    if format == "turtle":
        content = exporter.export_turtle()
        media_type = "text/turtle"
        ext = "ttl"
    elif format == "ntriples":
        content = exporter.export_ntriples()
        media_type = "application/n-triples"
        ext = "nt"
    elif format == "jsonld":
        content = exporter.export_jsonld()
        media_type = "application/ld+json"
        ext = "jsonld"
    else:  # xml
        content = exporter.export_rdfxml()
        media_type = "application/rdf+xml"
        ext = "rdf"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename=green_zones.{ext}"}
    )

