# GreenEduMap Resource Service - Test Script (curl)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Resource Service Testing" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "[1] Health Check..." -ForegroundColor Yellow
curl http://localhost:8002/health
Write-Host ""
Write-Host ""

# Test 2: Create Green Zone
Write-Host "[2] Creating Green Zone 'Sơn Trà'..." -ForegroundColor Yellow
$json = '{"name":"Khu vực xanh Sơn Trà","code":"GZ001","latitude":16.0544,"longitude":108.2022,"address":"Đà Nẵng","total_capacity":100,"is_public":true,"current_occupancy":0}'
curl -X POST http://localhost:8002/api/v1/centers/ -H "Content-Type: application/json" -d $json
Write-Host ""
Write-Host ""

# Test 3: List All Centers
Write-Host "[3] Listing all centers..." -ForegroundColor Yellow
curl http://localhost:8002/api/v1/centers/
Write-Host ""
Write-Host ""

# Test 4: Create Another Zone
Write-Host "[4] Creating Green Zone 'Mỹ Khê'..." -ForegroundColor Yellow
$json2 = '{"name":"Khu vực xanh Mỹ Khê","code":"GZ002","latitude":16.0394,"longitude":108.2302,"address":"Đà Nẵng","total_capacity":80,"is_public":true,"current_occupancy":0}'
curl -X POST http://localhost:8002/api/v1/centers/ -H "Content-Type: application/json" -d $json2
Write-Host ""
Write-Host ""

# Test 5: Nearby Search
Write-Host "[5] Finding centers near Đà Nẵng (10km radius)..." -ForegroundColor Yellow
curl "http://localhost:8002/api/v1/centers/nearby?latitude=16.05&longitude=108.22&radius_km=10"
Write-Host ""
Write-Host ""

# Test 6: Public OpenData Endpoint via Gateway
Write-Host "[6] Testing OpenData API via Gateway..." -ForegroundColor Yellow
curl http://localhost:8000/api/open-data/centers
Write-Host ""
Write-Host ""

Write-Host "=====================================" -ForegroundColor Green
Write-Host " Tests Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
