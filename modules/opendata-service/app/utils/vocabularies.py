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
Vocabularies and URIs for Linked Data
"""

# Standard Prefixes
PREFIXES = {
    "schema": "https://schema.org/",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcterms": "http://purl.org/dc/terms/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "vcard": "http://www.w3.org/2006/vcard/ns#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "ngsi-ld": "https://uri.etsi.org/ngsi-ld/",
}

# GreenEduMap specific
GEM_PREFIX = "http://greenedumap.vn/data/"
GEM_ONTOLOGY = "http://greenedumap.vn/ontology#"

# NGSI-LD Entity Types
NGSI_LD_TYPES = {
    "AirQualityObserved": "https://uri.fiware.org/ns/data-models#AirQualityObserved",
    "School": f"{GEM_ONTOLOGY}School",
    "GreenZone": f"{GEM_ONTOLOGY}GreenZone",
    "GreenCourse": f"{GEM_ONTOLOGY}GreenCourse",
    "WeatherObserved": "https://uri.fiware.org/ns/data-models#WeatherObserved",
}

# Property mappings
SCHEMA_ORG_PROPERTIES = {
    "name": "schema:name",
    "description": "schema:description",
    "address": "schema:address",
    "location": "schema:geo",
    "telephone": "schema:telephone",
    "email": "schema:email",
    "url": "schema:url",
}


def get_entity_uri(entity_type: str, entity_id: str) -> str:
    """Generate URI for an entity"""
    return f"{GEM_PREFIX}{entity_type}/{entity_id}"


def get_sparql_prefixes() -> str:
    """Get SPARQL PREFIX declarations"""
    return "\n".join([f"PREFIX {k}: <{v}>" for k, v in PREFIXES.items()])

