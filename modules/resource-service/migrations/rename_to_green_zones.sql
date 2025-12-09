-- GreenEduMap Resource Service Migration
-- Refactor from rescue_centers to green_zones

-- ================================================
-- Step 1: Rename tables
-- ================================================

ALTER TABLE IF EXISTS rescue_centers RENAME TO green_zones;
ALTER TABLE IF EXISTS resources RENAME TO green_resources;

-- ================================================
-- Step 2: Rename constraints and indexes
-- ================================================

-- Foreign key constraint
ALTER TABLE green_resources 
  DROP CONSTRAINT IF EXISTS resources_center_id_fkey;

ALTER TABLE green_resources 
  ADD CONSTRAINT green_resources_zone_id_fkey 
  FOREIGN KEY (center_id) REFERENCES green_zones(id) ON DELETE CASCADE;

-- ================================================
-- Step 3: Rename columns
-- ================================================

-- In green_zones table
ALTER TABLE green_zones 
  RENAME COLUMN total_capacity TO area_sqm;

ALTER TABLE green_zones 
  RENAME COLUMN current_occupancy TO tree_count;

ALTER TABLE green_zones 
  RENAME COLUMN manager_name TO maintained_by;

-- In green_resources table
ALTER TABLE green_resources 
  RENAME COLUMN center_id TO zone_id;

-- ================================================
-- Step 4: Add new columns
-- ================================================

ALTER TABLE green_zones 
  ADD COLUMN IF NOT EXISTS vegetation_coverage FLOAT;

ALTER TABLE green_zones 
  ADD COLUMN IF NOT EXISTS zone_type VARCHAR(50);

-- ================================================
-- Step 5: Update metadata for clarity
-- ================================================

-- Add comments to tables
COMMENT ON TABLE green_zones IS 'Green zones - parks, forests, gardens';
COMMENT ON TABLE green_resources IS 'Green resources - trees, solar panels, etc.';

-- Add comments to new columns
COMMENT ON COLUMN green_zones.zone_type IS 'Type: park, forest, garden, green_space';
COMMENT ON COLUMN green_zones.area_sqm IS 'Area in square meters';
COMMENT ON COLUMN green_zones.tree_count IS 'Number of trees in the zone';
COMMENT ON COLUMN green_zones.vegetation_coverage IS 'Vegetation coverage percentage (0-100)';
COMMENT ON COLUMN green_zones.maintained_by IS 'Organization maintaining the zone';

-- ================================================
-- Done!
-- ================================================
