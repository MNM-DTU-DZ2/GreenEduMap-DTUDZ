# GreenEduMap Docker Build Script
# Build và start services từ đầu (đã clean Docker trước đó)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " GreenEduMap - Docker Build & Start" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Set-Location infrastructure/docker

# 1. Build all services
Write-Host "[1/2] Building all services..." -ForegroundColor Yellow
Write-Host ""

docker-compose build --no-cache

Write-Host ""
Write-Host "[OK] All services built!" -ForegroundColor Green
Write-Host ""

# 2. Start services
Write-Host "[2/2] Starting services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host " Build Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

# Wait for services to be ready
Write-Host "Waiting 15 seconds for services to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "Quick Health Checks:" -ForegroundColor Yellow
Write-Host "- API Gateway: " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

Write-Host "- Auth Service: " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

Write-Host "- Resource Service: " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:8004/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

Write-Host "- Environment Service: " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:8007/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

Write-Host ""
Write-Host "View logs with:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f [service-name]" -ForegroundColor Gray
Write-Host ""
