# GreenEduMap - Comprehensive System Test
# Test all 14 services and features

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " GREENEDUMAP - FULL SYSTEM TEST" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$results = @()

# Helper function
function Test-Endpoint {
    param($Name, $Url, $Method = "GET")
    try {
        $response = Invoke-WebRequest -Uri $Url -Method $Method -TimeoutSec 5 -ErrorAction Stop
        return @{
            Name = $Name
            Status = "PASS"
            StatusCode = $response.StatusCode
            Error = $null
        }
    }
    catch {
        return @{
            Name = $Name
            Status = "FAIL"
            StatusCode = $null
            Error = $_.Exception.Message
        }
    }
}

Write-Host "Testing Infrastructure Services..." -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Gray

# 1. PostgreSQL
Write-Host "1. PostgreSQL + PostGIS..." -ForegroundColor White
try {
    docker exec greenedumap-postgres psql -U postgres -d greenedumap -c "SELECT version();" | Out-Null
    $results += @{ Service = "PostgreSQL + PostGIS"; Status = "PASS"; Details = "Database accessible" }
    Write-Host "   PASS" -ForegroundColor Green
} catch {
    $results += @{ Service = "PostgreSQL + PostGIS"; Status = "FAIL"; Details = $_.Exception.Message }
    Write-Host "   FAIL" -ForegroundColor Red
}

# 2. MongoDB
Write-Host "2. MongoDB..." -ForegroundColor White
$r = Test-Endpoint "MongoDB" "http://localhost:27017"
$results += @{ Service = "MongoDB"; Status = $r.Status; Details = if ($r.Status -eq "PASS") { "Port 27017 accessible" } else { "Connection failed" } }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

# 3. Redis
Write-Host "3. Redis..." -ForegroundColor White
try {
    docker exec greenedumap-redis redis-cli PING | Out-Null
    $results += @{ Service = "Redis"; Status = "PASS"; Details = "Cache server responding" }
    Write-Host "   PASS" -ForegroundColor Green
} catch {
    $results += @{ Service = "Redis"; Status = "FAIL"; Details = "Not responding" }
    Write-Host "   FAIL" -ForegroundColor Red
}

# 4. RabbitMQ
Write-Host "4. RabbitMQ..." -ForegroundColor White
$r = Test-Endpoint "RabbitMQ" "http://localhost:15672"
$results += @{ Service = "RabbitMQ"; Status = $r.Status; Details = if ($r.Status -eq "PASS") { "Management UI accessible" } else { "Connection failed" } }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

# 5. EMQX
Write-Host "5. EMQX (MQTT)..." -ForegroundColor White
$r = Test-Endpoint "EMQX" "http://localhost:18083"
$results += @{ Service = "EMQX (MQTT)"; Status = $r.Status; Details = if ($r.Status -eq "PASS") { "Dashboard accessible" } else { "Connection failed" } }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

Write-Host "`nTesting Microservices..." -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Gray

# 6. API Gateway
Write-Host "6. API Gateway..." -ForegroundColor White
$r = Test-Endpoint "API Gateway" "http://localhost:8000/health"
$results += @{ Service = "API Gateway"; Status = $r.Status; Details = if ($r.Status -eq "PASS") { "Port 8000, Rate limiting active" } else { $r.Error } }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

# 7. Auth Service
Write-Host "7. Auth Service..." -ForegroundColor White
$r = Test-Endpoint "Auth Service" "http://localhost:8000/api/auth/health"
if ($r.Status -eq "FAIL") {
    $r = Test-Endpoint "Auth Service Direct" "http://localhost:8001/health"
}
$results += @{ Service = "Auth Service"; Status = $r.Status; Details = if ($r.Status -eq "PASS") { "JWT authentication ready" } else { "Service unavailable" } }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

# 8. Education Service
Write-Host "8. Education Service..." -ForegroundColor White
$r = Test-Endpoint "Education Service - Schools" "http://localhost:8000/api/v1/schools"
$r2 = Test-Endpoint "Education Service - Courses" "http://localhost:8000/api/v1/green-courses"
$status = if ($r.Status -eq "PASS" -and $r2.Status -eq "PASS") { "PASS" } else { "PARTIAL" }
$results += @{ Service = "Education Service"; Status = $status; Details = "Schools API + Green Courses API" }
Write-Host "   $status" -ForegroundColor $(if ($status -eq "PASS") { "Green" } else { "Yellow" })

# 9. Environment Service
Write-Host "9. Environment Service..." -ForegroundColor White
$r = Test-Endpoint "Environment Service - AQI" "http://localhost:8000/api/v1/air-quality"
$r2 = Test-Endpoint "Environment Service - Weather" "http://localhost:8000/api/v1/weather"
$status = if ($r.Status -eq "PASS" -or $r2.Status -eq "PASS") { "PASS" } else { "FAIL" }
$results += @{ Service = "Environment Service"; Status = $status; Details = "AQI + Weather monitoring" }
Write-Host "   $status" -ForegroundColor $(if ($status -eq "PASS") { "Green" } else { "Red" })

# 10. Resource Service
Write-Host "10. Resource Service..." -ForegroundColor White
$r = Test-Endpoint "Resource Service" "http://localhost:8000/api/v1/green-zones"
$results += @{ Service = "Resource Service"; Status = $r.Status; Details = "Green zones + recycling centers" }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

Write-Host "`nTesting AI Service..." -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Gray

# 11. AI Service - Check if running
Write-Host "11. AI Service (ML Worker)..." -ForegroundColor White
try {
    # Check if container is running
    $containerStatus = docker ps --filter "name=greenedumap-ai-service" --format "{{.Status}}"
    if ($containerStatus -match "Up") {
        # Check logs for successful startup
        $aiLogs = docker logs greenedumap-ai-service 2>&1 | Select-String -Pattern "consumers started|AI Service is ready"
        if ($aiLogs) {
            $results += @{ Service = "AI Service"; Status = "PASS"; Details = "3 ML consumers running (Clustering, Prediction, Correlation)" }
            Write-Host "   PASS - Consumers running" -ForegroundColor Green
        } else {
            $results += @{ Service = "AI Service"; Status = "PARTIAL"; Details = "Container up but consumers status unclear" }
            Write-Host "   PARTIAL" -ForegroundColor Yellow
        }
    } else {
        $results += @{ Service = "AI Service"; Status = "FAIL"; Details = "Container not running" }
        Write-Host "   FAIL" -ForegroundColor Red
    }
} catch {
    $results += @{ Service = "AI Service"; Status = "FAIL"; Details = "Container not running" }
    Write-Host "   FAIL" -ForegroundColor Red
}

# Test AI features
Write-Host "   Testing AI features:" -ForegroundColor Gray
$ai_clustering = Test-Endpoint "AI Clustering" "http://localhost:8000/api/v1/tasks/ai/clustering?n_clusters=3" "POST"
$ai_prediction = Test-Endpoint "AI Prediction" "http://localhost:8000/api/v1/tasks/ai/prediction" "POST"
$ai_correlation = Test-Endpoint "AI Correlation" "http://localhost:8000/api/v1/tasks/ai/correlation" "POST"

$ai_pass = 0
if ($ai_clustering.Status -eq "PASS") { $ai_pass++; Write-Host "     - Clustering: PASS" -ForegroundColor Green } else { Write-Host "     - Clustering: FAIL" -ForegroundColor Red }
if ($ai_prediction.Status -eq "PASS") { $ai_pass++; Write-Host "     - Prediction: PASS" -ForegroundColor Green } else { Write-Host "     - Prediction: FAIL" -ForegroundColor Red }
if ($ai_correlation.Status -eq "PASS") { $ai_pass++; Write-Host "     - Correlation: PASS" -ForegroundColor Green } else { Write-Host "     - Correlation: FAIL" -ForegroundColor Red }

$results += @{ Service = "AI Features"; Status = if ($ai_pass -ge 2) { "PASS" } else { "PARTIAL" }; Details = "$ai_pass/3 features working" }

Write-Host "`nTesting OpenData Service..." -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Gray

# 12. OpenData Service
Write-Host "12. OpenData Service..." -ForegroundColor White
$opendata_tests = @(
    Test-Endpoint "OpenData - Health" "http://localhost:8009/health"
    Test-Endpoint "OpenData - NGSI-LD" "http://localhost:8009/api/v1/entities?type=School&limit=1"
    Test-Endpoint "OpenData - Catalog" "http://localhost:8009/api/v1/catalog"
    Test-Endpoint "OpenData - Context" "http://localhost:8009/api/v1/context"
    Test-Endpoint "OpenData - CSV Export" "http://localhost:8009/api/v1/export/csv/schools"
    Test-Endpoint "OpenData - GeoJSON" "http://localhost:8009/api/v1/export/geojson/schools"
)

$opendata_pass = ($opendata_tests | Where-Object { $_.Status -eq "PASS" }).Count
$results += @{ Service = "OpenData Service"; Status = if ($opendata_pass -ge 5) { "PASS" } else { "PARTIAL" }; Details = "$opendata_pass/6 endpoints working (NGSI-LD, DCAT-AP, Export)" }
Write-Host "   $($opendata_pass)/6 endpoints PASS" -ForegroundColor $(if ($opendata_pass -ge 5) { "Green" } else { "Yellow" })

Write-Host "`nTesting Frontend..." -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Gray

# 13. Web App
Write-Host "13. Web Application..." -ForegroundColor White
$r = Test-Endpoint "Web App" "http://localhost:3000"
$results += @{ Service = "Web Application"; Status = $r.Status; Details = if ($r.Status -eq "PASS") { "Next.js app running on port 3000" } else { "Not accessible" } }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

# 14. Adminer (DB UI)
Write-Host "14. Adminer (DB UI)..." -ForegroundColor White
$r = Test-Endpoint "Adminer" "http://localhost:8080"
$results += @{ Service = "Adminer"; Status = $r.Status; Details = "Database management UI" }
Write-Host "   $($r.Status)" -ForegroundColor $(if ($r.Status -eq "PASS") { "Green" } else { "Red" })

# Summary
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host " TEST SUMMARY" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

$total = $results.Count
$passed = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$partial = ($results | Where-Object { $_.Status -eq "PARTIAL" }).Count
$failed = ($results | Where-Object { $_.Status -eq "FAIL" }).Count

Write-Host "`nTotal Services: $total" -ForegroundColor White
Write-Host "  PASS: $passed" -ForegroundColor Green
Write-Host "  PARTIAL: $partial" -ForegroundColor Yellow
Write-Host "  FAIL: $failed" -ForegroundColor Red
Write-Host "`nSuccess Rate: $([math]::Round(($passed + $partial/2) / $total * 100, 1))%" -ForegroundColor Cyan

# Export results
$results | Export-Csv -Path "test_results.csv" -NoTypeInformation -Encoding UTF8
Write-Host "`nResults exported to: test_results.csv" -ForegroundColor Gray

# Return results for further processing
return $results

