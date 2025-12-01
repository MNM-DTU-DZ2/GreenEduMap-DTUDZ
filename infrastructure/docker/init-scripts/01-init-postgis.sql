-- Initialize PostGIS extension for GreenEduMap
-- This script runs automatically on first PostgreSQL startup

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Verify PostGIS installation
SELECT PostGIS_Version();

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE greenedumap TO postgres;

-- Log success
DO $$
BEGIN
    RAISE NOTICE 'PostGIS extension enabled successfully for GreenEduMap';
END $$;
