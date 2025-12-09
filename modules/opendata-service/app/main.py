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
OpenData Service - Main Application
Provides NGSI-LD entities, DCAT-AP catalog, and multiple export formats
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import entities, catalog, context, export

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="""
    ## GreenEduMap - OpenData Service
    
    Open data portal for environmental education in Vietnam.
    
    ### Features:
    - **NGSI-LD Entities**: Standard format for smart cities data
    - **DCAT-AP Catalog**: Data catalog vocabulary
    - **Multiple Exports**: CSV, GeoJSON, RDF (Turtle, N-Triples, JSON-LD)
    - **Linked Data**: Full RDF support with vocabularies
    
    ### Datasets:
    - Schools with Green Scores
    - Air Quality Observations
    - Green Zones (Parks, Forests)
    - Environmental Education Courses
    
    ### Standards:
    - NGSI-LD (ETSI GS CIM 009)
    - DCAT-AP 2.0
    - JSON-LD 1.1
    - GeoJSON (RFC 7946)
    - RDF 1.1 (Turtle, N-Triples, JSON-LD, RDF/XML)
    """
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "description": "Open Data & Export API for GreenEduMap",
        "standards": [
            "NGSI-LD",
            "DCAT-AP 2.0",
            "JSON-LD 1.1",
            "GeoJSON",
            "RDF 1.1"
        ],
        "endpoints": {
            "entities": f"{settings.API_V1_STR}/entities",
            "catalog": f"{settings.API_V1_STR}/catalog",
            "context": f"{settings.API_V1_STR}/context",
            "export": f"{settings.API_V1_STR}/export",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "opendata-service",
        "version": settings.VERSION
    }


# Include routers
app.include_router(entities.router, prefix=settings.API_V1_STR)
app.include_router(catalog.router, prefix=settings.API_V1_STR)
app.include_router(context.router, prefix=settings.API_V1_STR)
app.include_router(export.router, prefix=settings.API_V1_STR)

