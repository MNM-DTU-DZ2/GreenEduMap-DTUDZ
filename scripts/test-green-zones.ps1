# Test GreenEduMap Green Zones API
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Green Zones API Testing" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "[1] Health Check..." -ForegroundColor Yellow
curl http://localhost:8002/health
Write-Host "`n"

# Test 2: Create Green Zone - Công viên Sơn Trà
Write-Host "[2] Creating Green Zone 'Công viên Sơn Trà'..." -ForegroundColor Yellow
$json1 = '{"name":"Công viên Sơn Trà","code":"GZ-ST-001","latitude":16.0544,"longitude":108.2022,"address":"Đà Nẵng","zone_type":"park","area_sqm":50000,"tree_count":1200,"vegetation_coverage":85.5,"maintained_by":"Sở Xây dựng Đà Nẵng","is_public":true}'
curl -X POST http://localhost:8002/api/v1/green-zones/ -H "Content-Type: application/json" -d $json1
Write-Host "`n"

# Test 3: Create Another Zone - Vườn cây Mỹ Khê
Write-Host "[3] Creating Green Zone 'Vườn cây Mỹ Khê'..." -ForegroundColor Yellow
$json2 = '{"name":"Vườn cây Mỹ Khê","code":"GZ-MK-001","latitude":16.0394,"longitude":108.2302,"address":"Đà Nẵng","zone_type":"garden","area_sqm":30000,"tree_count":800,"vegetation_coverage":75.0,"is_public":true}'
curl -X POST http://localhost:8002/api/v1/green-zones/ -H "Content-Type: application/json" -d $json2
Write-Host "`n"

# Test 4: List All Zones
Write-Host "[4] List all green zones..." -ForegroundColor Yellow
curl http://localhost:8002/api/v1/green-zones/
Write-Host "`n"

# Test 5: Nearby Search
Write-Host "[5] Finding zones near Đà Nẵng (10km radius)..." -ForegroundColor Yellow
curl "http://localhost:8002/api/v1/green-zones/nearby?latitude=16.05&longitude=108.22&radius_km=10"
Write-Host "`n"

# Test 6: OpenData via Gateway
Write-Host "[6] Testing OpenData API (via Gateway)..." -ForegroundColor Yellow
curl http://localhost:8000/api/open-data/green-zones
Write-Host "`n"

Write-Host "=====================================" -ForegroundColor Green
Write-Host " Tests Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
