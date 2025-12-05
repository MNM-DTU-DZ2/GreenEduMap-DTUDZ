-- Green Zones and Green Resources tables for Resource Service
-- Run after PostGIS is enabled

-- Green Zones table
CREATE TABLE IF NOT EXISTS green_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    address VARCHAR(1000),
    zone_type VARCHAR(50),  -- park, forest, garden, green_space
    area_sqm INTEGER,
    tree_count INTEGER DEFAULT 0,
    vegetation_coverage NUMERIC(5, 2),  -- 0-100%
    maintained_by VARCHAR(255),
    phone VARCHAR(20),
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    data_uri VARCHAR(500),
    ngsi_ld_uri VARCHAR(500),
    facilities JSONB,
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_green_zones_location ON green_zones USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_green_zones_code ON green_zones(code);
CREATE INDEX IF NOT EXISTS idx_green_zones_type ON green_zones(zone_type);

-- Green Resources table (matches resource-service model)
CREATE TABLE IF NOT EXISTS green_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- trees, solar_panels, wind_turbines, recycling_bins
    quantity INTEGER DEFAULT 0 NOT NULL,
    available_quantity INTEGER DEFAULT 0 NOT NULL,
    unit VARCHAR(50) NOT NULL,  -- pieces, kWh, kg
    zone_id UUID REFERENCES green_zones(id) ON DELETE CASCADE NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    expiry_date TIMESTAMPTZ,
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    data_uri VARCHAR(500),
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_green_resources_zone_id ON green_resources(zone_id);
CREATE INDEX IF NOT EXISTS idx_green_resources_type ON green_resources(type);

-- Insert sample data for testing
INSERT INTO green_zones (name, code, location, address, zone_type, area_sqm, tree_count, vegetation_coverage, maintained_by)
VALUES 
    ('Công viên Tao Đàn', 'GZ-001', ST_GeogFromText('SRID=4326;POINT(106.6948 10.7758)'), '55B Nguyễn Thị Minh Khai, Q.1, TP.HCM', 'park', 100000, 500, 75.5, 'Sở Xây dựng TP.HCM'),
    ('Vườn Bách Thảo', 'GZ-002', ST_GeogFromText('SRID=4326;POINT(106.7019 10.7685)'), '1 Nguyễn Bỉnh Khiêm, Q.1, TP.HCM', 'garden', 50000, 200, 60.0, 'Sở Nông nghiệp'),
    ('Công viên 23/9', 'GZ-003', ST_GeogFromText('SRID=4326;POINT(106.6931 10.7712)'), 'Phạm Ngũ Lão, Q.1, TP.HCM', 'park', 80000, 350, 65.0, 'UBND Quận 1')
ON CONFLICT (code) DO NOTHING;

-- Insert green resources with correct schema
INSERT INTO green_resources (name, type, quantity, available_quantity, unit, zone_id, status)
SELECT 'Cây xanh khu A', 'tree', 100, 90, 'pieces', gz.id, 'active'
FROM green_zones gz WHERE gz.code = 'GZ-001'
ON CONFLICT DO NOTHING;

INSERT INTO green_resources (name, type, quantity, available_quantity, unit, zone_id, status)
SELECT 'Thùng rác tái chế', 'recycling_bin', 20, 18, 'pieces', gz.id, 'active'
FROM green_zones gz WHERE gz.code = 'GZ-001'
ON CONFLICT DO NOTHING;

INSERT INTO green_resources (name, type, quantity, available_quantity, unit, zone_id, status)
SELECT 'Tấm pin năng lượng mặt trời', 'solar_panel', 50, 50, 'pieces', gz.id, 'active'
FROM green_zones gz WHERE gz.code = 'GZ-002'
ON CONFLICT DO NOTHING;

-- Log success
DO $$
BEGIN
    RAISE NOTICE 'Green zones and resources tables created with sample data';
END $$;
