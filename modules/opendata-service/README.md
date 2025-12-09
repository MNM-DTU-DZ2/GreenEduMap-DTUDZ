# OpenData Service - GreenEduMap

## 🌐 Overview

OpenData Service provides **open access** to GreenEduMap data in multiple standard formats:
- **NGSI-LD**: Smart cities standard
- **DCAT-AP**: Data catalog vocabulary
- **CSV**: Spreadsheet format
- **GeoJSON**: Geographic data
- **RDF**: Linked Data (Turtle, N-Triples, JSON-LD, RDF/XML)

---

## 🎯 Features

### 1. NGSI-LD Entities
Standard format cho Smart Cities data:
- AirQualityObserved
- School
- GreenZone
- GreenCourse

### 2. DCAT-AP Catalog
Data catalog với metadata đầy đủ:
- Dataset descriptions
- Distribution formats
- Access URLs
- License information

### 3. Multiple Export Formats
Download data trong nhiều format:
- **CSV**: Excel, data analysis
- **GeoJSON**: GIS tools (QGIS, ArcGIS)
- **RDF Turtle**: Linked Data
- **RDF N-Triples**: Triple stores
- **JSON-LD**: Semantic Web
- **RDF/XML**: Legacy systems

---

## 📡 API Endpoints

### NGSI-LD Entities
```bash
GET /api/v1/entities
GET /api/v1/entities?type=School
GET /api/v1/entities?type=AirQualityObserved
GET /api/v1/entities/{id}
```

### DCAT-AP Catalog
```bash
GET /api/v1/catalog
GET /api/v1/catalog/datasets
GET /api/v1/catalog/datasets/{id}
```

### JSON-LD Context
```bash
GET /api/v1/context
```

### Export - CSV
```bash
GET /api/v1/export/csv/schools
GET /api/v1/export/csv/air-quality
GET /api/v1/export/csv/green-zones
GET /api/v1/export/csv/green-courses
```

### Export - GeoJSON
```bash
GET /api/v1/export/geojson/schools
GET /api/v1/export/geojson/air-quality
GET /api/v1/export/geojson/green-zones
```

### Export - RDF
```bash
GET /api/v1/export/rdf/schools?format=turtle
GET /api/v1/export/rdf/air-quality?format=ntriples
GET /api/v1/export/rdf/green-zones?format=jsonld
```

---

## 🚀 Quick Start

### Run with Docker
```bash
cd infrastructure/docker
docker compose up -d opendata-service
```

### Access Service
- **API**: http://localhost:8009
- **Docs**: http://localhost:8009/docs
- **Health**: http://localhost:8009/health

---

## 📊 Example Usage

### Get NGSI-LD Schools
```bash
curl http://localhost:8009/api/v1/entities?type=School
```

### Download Schools CSV
```bash
curl -O http://localhost:8009/api/v1/export/csv/schools
```

### Download Schools GeoJSON
```bash
curl -O http://localhost:8009/api/v1/export/geojson/schools
```

### Download Schools RDF (Turtle)
```bash
curl "http://localhost:8009/api/v1/export/rdf/schools?format=turtle" -o schools.ttl
```

### Get DCAT-AP Catalog
```bash
curl http://localhost:8009/api/v1/catalog
```

---

## 🔗 Standards Compliance

### NGSI-LD
- **Spec**: ETSI GS CIM 009 V1.6.1
- **Context**: https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld
- **Properties**: type, value, observedAt, unitCode
- **GeoProperty**: GeoJSON geometry

### DCAT-AP
- **Version**: 2.1.1
- **Vocabularies**: DCAT, DCTERMS, FOAF, VCARD
- **Classes**: Catalog, Dataset, Distribution

### JSON-LD
- **Version**: 1.1
- **Vocabularies**: schema.org, GeoSPARQL, dcterms

### GeoJSON
- **Spec**: RFC 7946
- **CRS**: EPSG:4326 (WGS 84)
- **Geometry**: Point

### RDF
- **Formats**: Turtle, N-Triples, JSON-LD, RDF/XML
- **Vocabularies**: schema.org, geo, dcterms, custom GreenEduMap ontology

---

## 🎓 OLP 2025 Demo

OpenData Service thể hiện:
- ✅ **Interoperability**: Chuẩn quốc tế (NGSI-LD, DCAT-AP)
- ✅ **Open Data**: Public access, multiple formats
- ✅ **Linked Data**: RDF, vocabularies, semantics
- ✅ **GIS Integration**: GeoJSON cho QGIS, ArcGIS
- ✅ **Data Catalog**: DCAT-AP metadata

**Demo Flow**:
1. Show DCAT-AP catalog → Datasets overview
2. Download CSV → Excel analysis
3. Download GeoJSON → Import vào QGIS
4. Show NGSI-LD → Smart Cities standard
5. Show RDF Turtle → Linked Data

---

## 📚 Documentation

- API Docs: http://localhost:8009/docs
- ReDoc: http://localhost:8009/redoc

---

## 🛠️ Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
cd modules/opendata-service
uvicorn app.main:app --reload --port 8009
```

---

## 🌟 Key Achievements

- ✅ NGSI-LD compliant entities
- ✅ DCAT-AP 2.1 catalog
- ✅ 4 datasets (Schools, AQI, Zones, Courses)
- ✅ 5 export formats (CSV, GeoJSON, 3 RDF formats)
- ✅ Full vocabulary mapping (schema.org, geo, dcterms)
- ✅ OLP 2025 ready

---

**Status**: 🎉 Production Ready for OLP 2025

