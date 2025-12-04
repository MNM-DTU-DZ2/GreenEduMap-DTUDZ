# GreenEduMap Database Seeder PowerShell Script
# Windows-friendly version

param(
    [switch]$y,
    [switch]$AutoConfirm
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " GreenEduMap Database Seeder" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "OK Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "ERROR Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if PostgreSQL container is running
Write-Host "Checking PostgreSQL container..." -ForegroundColor Yellow
$postgresRunning = docker ps --filter "name=greenedumap-postgres" --format "{{.Names}}"
if ($postgresRunning) {
    Write-Host "OK PostgreSQL container is running" -ForegroundColor Green
}
else {
    Write-Host "ERROR PostgreSQL container is not running" -ForegroundColor Red
    Write-Host "  Run: docker-compose up -d postgres" -ForegroundColor Gray
    exit 1
}

Write-Host ""

# Check if auto-confirm is enabled
if (-not $y -and -not $AutoConfirm) {
    Write-Host "This will populate the database with sample data." -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continue? (y/N)"

    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Cancelled" -ForegroundColor Red
        exit 0
    }
}
else {
    Write-Host "Auto-confirm enabled, seeding database..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Seeding Database" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to execute SQL file in container
function Execute-SqlFile {
    param(
        [string]$ServiceName,
        [string]$FilePath
    )
    
    Write-Host ""
    Write-Host "[$ServiceName]" -ForegroundColor Cyan
    
    if (Test-Path $FilePath) {
        Write-Host "  Loading: $FilePath" -ForegroundColor Gray
        
        # Copy file to container and execute
        $containerPath = "/tmp/seed_$(Get-Random).sql"
        docker cp $FilePath greenedumap-postgres:$containerPath | Out-Null
        
        # Temporarily allow errors
        $prevErrorPref = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        
        $result = docker exec greenedumap-postgres psql -U postgres -d greenedumap -f $containerPath 2>&1
        
        $ErrorActionPreference = $prevErrorPref
        
        # Check if there are real errors (not just NOTICE or WARNING)
        $hasError = $false
        foreach ($line in $result) {
            if ($line -match "ERROR:") {
                $hasError = $true
                Write-Host "  ! $line" -ForegroundColor Red
            }
        }
        
        if (-not $hasError) {
            Write-Host "  OK Successfully seeded" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "  ERROR: Failed to seed data" -ForegroundColor Red
            return $false
        }
    }
    else {
        Write-Host "  ERROR File not found: $FilePath" -ForegroundColor Red
        return $false
    }
}

# Seed files
$seedFiles = @(
    @{ Name = "Education Service"; Path = "modules\education-service\migrations\seed_data.sql" },
    @{ Name = "Resource Service"; Path = "modules\resource-service\migrations\seed_data.sql" },
    @{ Name = "Environment Service"; Path = "modules\environment-service\seed_data.sql" }
)

$successCount = 0
foreach ($seed in $seedFiles) {
    if (Execute-SqlFile -ServiceName $seed.Name -FilePath $seed.Path) {
        $successCount++
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Data Statistics" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get row counts
$tables = @('schools', 'green_courses', 'green_activities', 'green_zones', 'centers', 'green_resources', 'air_quality_data', 'weather_data')

foreach ($table in $tables) {
    $query = "SELECT COUNT(*) FROM $table;"
    $count = docker exec greenedumap-postgres psql -U postgres -d greenedumap -t -c $query 2>$null
    if ($count) {
        $count = $count.Trim()
        Write-Host "  ${table}: $count rows" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " Seeding Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Services seeded: $successCount/$($seedFiles.Count)" -ForegroundColor Gray
Write-Host ""
Write-Host "  You can now test the API endpoints" -ForegroundColor Yellow
Write-Host ""

