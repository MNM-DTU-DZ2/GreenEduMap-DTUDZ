$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Test-Endpoint {
    param($Url, $Method = "GET")
    Write-Host "Testing $Method $Url..." -NoNewline
    try {
        $response = Invoke-RestMethod -Uri $Url -Method $Method
        Write-Host " [OK]" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host " [FAILED]" -ForegroundColor Red
        Write-Host $_.Exception.Message
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader $_.Exception.Response.GetResponseStream()
            Write-Host $reader.ReadToEnd()
        }
        return $null
    }
}

Write-Host "`n=== API Gateway & OpenData E2E Tests ===`n" -ForegroundColor Cyan

# 1. Gateway Health Check
Write-Host "=== 1. Gateway Health Check ===" -ForegroundColor Cyan
$health = Test-Endpoint "http://localhost:8000/health"

if ($health) {
    Write-Host "  Gateway Status: $($health.status)" -ForegroundColor Yellow
    Write-Host "  Education Service: $($health.services.education)" -ForegroundColor Yellow
    
    if ($health.services.education -eq "healthy") {
        Write-Host "  [SUCCESS] Education Service is healthy via Gateway" -ForegroundColor Green
    }
    else {
        Write-Host "  [FAILURE] Education Service is NOT healthy" -ForegroundColor Red
    }
}

# 2. Education Service Proxy (Private API)
Write-Host "`n=== 2. Education Service Proxy (Private API) ===" -ForegroundColor Cyan
$schools = Test-Endpoint "http://localhost:8000/api/v1/schools?limit=5"

if ($schools) {
    Write-Host "  Retrieved $($schools.Count) schools via Gateway" -ForegroundColor Yellow
    if ($schools.Count -gt 0) {
        Write-Host "  First School: $($schools[0].name)" -ForegroundColor Yellow
        Write-Host "  [SUCCESS] Proxy working for /api/v1/schools" -ForegroundColor Green
    }
}

# 3. OpenData API (GeoJSON)
Write-Host "`n=== 3. OpenData API (GeoJSON) ===" -ForegroundColor Cyan
$geojson = Test-Endpoint "http://localhost:8000/api/open-data/schools?format=geojson&limit=5"

if ($geojson) {
    Write-Host "  Type: $($geojson.type)" -ForegroundColor Yellow
    Write-Host "  Features: $($geojson.features.Count)" -ForegroundColor Yellow
    
    if ($geojson.type -eq "FeatureCollection" -and $geojson.features.Count -gt 0) {
        $firstFeature = $geojson.features[0]
        Write-Host "  First Feature: $($firstFeature.properties.name)" -ForegroundColor Yellow
        Write-Host "  Geometry Type: $($firstFeature.geometry.type)" -ForegroundColor Yellow
        Write-Host "  [SUCCESS] OpenData GeoJSON endpoint working" -ForegroundColor Green
    }
    else {
        Write-Host "  [FAILURE] Invalid GeoJSON response" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "E2E Tests Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green
