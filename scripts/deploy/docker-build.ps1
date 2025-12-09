# GreenEduMap Docker Build Script
# Build and start services from scratch

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " GreenEduMap - Docker Build & Start" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Get current directory and navigate
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Item -Path "$ScriptDir\..\..").FullName
$DockerDir = "$ProjectRoot\infrastructure\docker"
Set-Location $DockerDir

# ================================
# Environment Setup
# ================================
Write-Host "[0/5] Setting up environment..." -ForegroundColor Yellow

# Check for environment file
$envFile = ".env.local"
if (-not (Test-Path $envFile)) {
    Write-Host ""
    Write-Host "WARNING: $envFile not found!" -ForegroundColor Red
    Write-Host "Creating from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" $envFile
    Write-Host "✓ Created $envFile" -ForegroundColor Green
    Write-Host "  Review and adjust settings if needed" -ForegroundColor Gray
} else {
    Write-Host "✓ Using existing $envFile" -ForegroundColor Green
}

Write-Host ""

# 1. Build all services
Write-Host "[1/5] Building all services..." -ForegroundColor Yellow
Write-Host ""

docker-compose --env-file $envFile build --no-cache

Write-Host ""
Write-Host "[OK] All services built!" -ForegroundColor Green
Write-Host ""

# 2. Start services
Write-Host "[2/5] Starting services..." -ForegroundColor Yellow
docker-compose --env-file $envFile up -d

Write-Host ""
Write-Host "[OK] Services started!" -ForegroundColor Green
Write-Host ""

# Wait for services to be ready
Write-Host "Waiting 20 seconds for services to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 20

Write-Host ""
Write-Host "Service Status:" -ForegroundColor Cyan
docker-compose --env-file $envFile ps

# Read ports from .env file
$apiPort = (Get-Content $envFile | Select-String "^API_GATEWAY_PORT=").ToString().Split("=")[1]
$resourcePort = (Get-Content $envFile | Select-String "^RESOURCE_SERVICE_PORT=").ToString().Split("=")[1]
$educationPort = (Get-Content $envFile | Select-String "^EDUCATION_SERVICE_PORT=").ToString().Split("=")[1]
$opendataPort = (Get-Content $envFile | Select-String "^OPENDATA_SERVICE_PORT=").ToString().Split("=")[1]

if (-not $apiPort) { $apiPort = "4500" }
if (-not $resourcePort) { $resourcePort = "4304" }
if (-not $educationPort) { $educationPort = "4302" }
if (-not $opendataPort) { $opendataPort = "4305" }

Write-Host ""
Write-Host "Quick Health Checks:" -ForegroundColor Yellow
Write-Host "- API Gateway (port $apiPort): " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:$apiPort/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

Write-Host "- Resource Service (port $resourcePort): " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:$resourcePort/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

Write-Host "- Education Service (port $educationPort): " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:$educationPort/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

Write-Host "- OpenData Service (port $opendataPort): " -NoNewline
try { 
    $response = Invoke-RestMethod -Uri "http://localhost:$opendataPort/health" -TimeoutSec 3
    Write-Host "OK" -ForegroundColor Green 
} catch { 
    Write-Host "FAILED" -ForegroundColor Red 
}

# 3. Wait for database to be ready
Write-Host ""
Write-Host "[3/5] Preparing database..." -ForegroundColor Yellow

$POSTGRES_CONTAINER = "greenedumap-postgres"
$POSTGRES_USER = "postgres"
$POSTGRES_DB = "greenedumap"

# Wait for PostgreSQL to be ready
Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Cyan
$maxAttempts = 30
$attempt = 0
$pgReady = $false

while ($attempt -lt $maxAttempts -and -not $pgReady) {
    try {
        $result = docker exec $POSTGRES_CONTAINER pg_isready -U $POSTGRES_USER 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pgReady = $true
            Write-Host "PostgreSQL is ready!" -ForegroundColor Green
        }
    } catch {
        # Continue waiting
    }
    
    if (-not $pgReady) {
        $attempt++
        Start-Sleep -Seconds 1
    }
}

if (-not $pgReady) {
    Write-Host "PostgreSQL did not become ready in time" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "INFO: Init scripts (01-04) are auto-executed by PostgreSQL on first startup" -ForegroundColor Cyan
Write-Host "      Location: infrastructure/docker/init-scripts/" -ForegroundColor Gray
Write-Host ""
Write-Host "[OK] Database initialized!" -ForegroundColor Green

# 4. Seed database (optional sample data)
Write-Host ""
Write-Host "[4/5] Seeding sample data..." -ForegroundColor Yellow

# Function to execute SQL file
function Execute-SqlFile {
    param(
        [string]$ServiceName,
        [string]$FilePath
    )
    
    Write-Host ""
    Write-Host "[$ServiceName]" -ForegroundColor Cyan
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "  WARNING: File not found, skipping..." -ForegroundColor Yellow
        return $false
    }
    
    $fileName = Split-Path -Leaf $FilePath
    Write-Host "  Loading: $fileName" -ForegroundColor Gray
    
    # Copy file to container
    $timestamp = Get-Date -Format 'yyyyMMddHHmmss'
    $containerPath = "/tmp/seed_$timestamp.sql"
    docker cp $FilePath "${POSTGRES_CONTAINER}:${containerPath}" | Out-Null
    
    # Execute SQL (redirect stderr to capture output, then filter)
    $result = docker exec $POSTGRES_CONTAINER psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f $containerPath 2>&1 | 
              Where-Object { $_ -notmatch "NOTICE:" -and $_ -notmatch "WARNING:" }
    
    # Check for errors
    if ($result -match "ERROR:") {
        $errorLine = $result | Select-String 'ERROR:' | Select-Object -First 1
        Write-Host "  ERROR: $errorLine" -ForegroundColor Red
        return $false
    } else {
        Write-Host "  SUCCESS: Data seeded" -ForegroundColor Green
        return $true
    }
}

$seedScripts = @(
    @{Path="$ProjectRoot\modules\education-service\migrations\seed_data.sql"; Name="Education Service"},
    @{Path="$ProjectRoot\modules\resource-service\migrations\seed_data.sql"; Name="Resource Service"}
)

$successCount = 0
foreach ($script in $seedScripts) {
    if (Execute-SqlFile -ServiceName $script.Name -FilePath $script.Path) {
        $successCount++
    }
}

$totalScripts = $seedScripts.Count
Write-Host ""
Write-Host "[OK] Seeding completed! ($successCount/$totalScripts successful)" -ForegroundColor Green

# 5. Display statistics
Write-Host ""
Write-Host "[5/5] Database Statistics..." -ForegroundColor Yellow

$tables = @('schools', 'green_courses', 'green_zones', 'green_resources', 'air_quality', 'weather', 'green_activities')

foreach ($table in $tables) {
    try {
        $query = "SELECT COUNT(*) FROM $table;"
        $count = docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -t -c $query 2>$null
        if ($count) {
            $count = $count.Trim()
            if ($count -ne '0') {
                Write-Host "  $table : $count rows" -ForegroundColor Green
            }
        }
    } catch {
        # Table might not exist, skip
    }
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host " Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "View logs with:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f SERVICE_NAME" -ForegroundColor Gray
Write-Host ""
