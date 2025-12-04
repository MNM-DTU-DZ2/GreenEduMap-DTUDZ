"""
RDF Export Service (Turtle, N-Triples, JSON-LD)
"""
from typing import List, Dict, Any
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, GEO
from app.utils.vocabularies import PREFIXES, GEM_PREFIX, GEM_ONTOLOGY


class RDFExporter:
    """Export data to RDF formats"""
    
    def __init__(self):
        self.graph = Graph()
        
        # Bind prefixes
        self.gem = Namespace(GEM_PREFIX)
        self.gem_ont = Namespace(GEM_ONTOLOGY)
        self.schema = Namespace("https://schema.org/")
        
        self.graph.bind("gem", self.gem)
        self.graph.bind("gem-ont", self.gem_ont)
        self.graph.bind("schema", self.schema)
        self.graph.bind("dcterms", DCTERMS)
        self.graph.bind("geo", GEO)
    
    def add_school(self, school: Dict[str, Any]):
        """Add school to RDF graph"""
        school_uri = URIRef(f"{GEM_PREFIX}School/{school['id']}")
        
        # Type
        self.graph.add((school_uri, RDF.type, self.gem_ont.School))
        self.graph.add((school_uri, RDF.type, self.schema.EducationalOrganization))
        
        # Properties
        if school.get("name"):
            self.graph.add((school_uri, self.schema.name, Literal(school["name"])))
        
        if school.get("code"):
            self.graph.add((school_uri, self.gem_ont.code, Literal(school["code"])))
        
        if school.get("address"):
            self.graph.add((school_uri, self.schema.address, Literal(school["address"])))
        
        # Geo
        if school.get("latitude") and school.get("longitude"):
            self.graph.add((school_uri, GEO.lat, Literal(school["latitude"], datatype=XSD.decimal)))
            self.graph.add((school_uri, GEO.long, Literal(school["longitude"], datatype=XSD.decimal)))
        
        # Green Score
        if school.get("green_score") is not None:
            self.graph.add((school_uri, self.gem_ont.greenScore, Literal(school["green_score"], datatype=XSD.decimal)))
        
        # Students & Teachers
        if school.get("total_students") is not None:
            self.graph.add((school_uri, self.gem_ont.totalStudents, Literal(school["total_students"], datatype=XSD.integer)))
        
        if school.get("total_teachers") is not None:
            self.graph.add((school_uri, self.gem_ont.totalTeachers, Literal(school["total_teachers"], datatype=XSD.integer)))
        
        # Type
        if school.get("type"):
            self.graph.add((school_uri, self.gem_ont.schoolType, Literal(school["type"])))
    
    def add_air_quality(self, aqi: Dict[str, Any]):
        """Add air quality observation to RDF graph"""
        aqi_uri = URIRef(f"{GEM_PREFIX}AirQualityObserved/{aqi['id']}")
        
        # Type
        self.graph.add((aqi_uri, RDF.type, self.gem_ont.AirQualityObservation))
        
        # AQI value
        if aqi.get("aqi") is not None:
            self.graph.add((aqi_uri, self.gem_ont.aqi, Literal(aqi["aqi"], datatype=XSD.decimal)))
        
        # Pollutants
        if aqi.get("pm25") is not None:
            self.graph.add((aqi_uri, self.gem_ont.pm25, Literal(aqi["pm25"], datatype=XSD.decimal)))
        
        if aqi.get("pm10") is not None:
            self.graph.add((aqi_uri, self.gem_ont.pm10, Literal(aqi["pm10"], datatype=XSD.decimal)))
        
        # Location
        if aqi.get("latitude") and aqi.get("longitude"):
            self.graph.add((aqi_uri, GEO.lat, Literal(aqi["latitude"], datatype=XSD.decimal)))
            self.graph.add((aqi_uri, GEO.long, Literal(aqi["longitude"], datatype=XSD.decimal)))
        
        # Station
        if aqi.get("station_name"):
            self.graph.add((aqi_uri, self.gem_ont.stationName, Literal(aqi["station_name"])))
        
        # Date
        if aqi.get("measurement_date"):
            self.graph.add((aqi_uri, DCTERMS.date, Literal(aqi["measurement_date"], datatype=XSD.dateTime)))
    
    def add_green_zone(self, zone: Dict[str, Any]):
        """Add green zone to RDF graph"""
        zone_uri = URIRef(f"{GEM_PREFIX}GreenZone/{zone['id']}")
        
        # Type
        self.graph.add((zone_uri, RDF.type, self.gem_ont.GreenZone))
        self.graph.add((zone_uri, RDF.type, self.schema.Park))
        
        # Properties
        if zone.get("name"):
            self.graph.add((zone_uri, self.schema.name, Literal(zone["name"])))
        
        if zone.get("description"):
            self.graph.add((zone_uri, self.schema.description, Literal(zone["description"])))
        
        if zone.get("zone_type"):
            self.graph.add((zone_uri, self.gem_ont.zoneType, Literal(zone["zone_type"])))
        
        # Geo
        if zone.get("latitude") and zone.get("longitude"):
            self.graph.add((zone_uri, GEO.lat, Literal(zone["latitude"], datatype=XSD.decimal)))
            self.graph.add((zone_uri, GEO.long, Literal(zone["longitude"], datatype=XSD.decimal)))
        
        # Area
        if zone.get("area_sqm") is not None:
            self.graph.add((zone_uri, self.gem_ont.areaSqm, Literal(zone["area_sqm"], datatype=XSD.decimal)))
    
    def export_turtle(self) -> str:
        """Export graph as Turtle"""
        return self.graph.serialize(format='turtle')
    
    def export_ntriples(self) -> str:
        """Export graph as N-Triples"""
        return self.graph.serialize(format='nt')
    
    def export_jsonld(self) -> str:
        """Export graph as JSON-LD"""
        return self.graph.serialize(format='json-ld', indent=2)
    
    def export_rdfxml(self) -> str:
        """Export graph as RDF/XML"""
        return self.graph.serialize(format='xml')

