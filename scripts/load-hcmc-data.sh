#!/bin/bash
#!/bin/bash
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

#
# Reset database and load HCMC seed data
#

echo "🔄 Resetting database with HCMC data..."

# Database connection
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-greenedumap}"
DB_USER="${POSTGRES_USER:-postgres}"

# Run seed files
echo "📚 Loading schools data..."
docker exec greenedumap-postgres psql -U $DB_USER -d $DB_NAME -f /docker-entrypoint-initdb.d/seed_data_hcmc_schools.sql

echo "🌳 Loading environment data..."
docker exec greenedumap-postgres psql -U $DB_USER -d $DB_NAME -f /docker-entrypoint-initdb.d/seed_data_hcmc_env.sql

echo "✅ HCMC data loaded successfully!"
echo ""
echo "📊 Verification:"
docker exec greenedumap-postgres psql -U $DB_USER -d $DB_NAME -c "
SELECT 'Schools' as table_name, COUNT(*) as count FROM schools
UNION ALL
SELECT 'Green Zones', COUNT(*) FROM green_zones
UNION ALL
SELECT 'Air Quality', COUNT(*) FROM air_quality
UNION ALL
SELECT 'Weather', COUNT(*) FROM weather
UNION ALL
SELECT 'Solar Resources', COUNT(*) FROM solar_resources;
"
