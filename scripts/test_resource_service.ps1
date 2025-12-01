$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Test-Endpoint {
    param($Url, $Method="GET", $Body=$null, $Headers=@{})
    Write-Host "Testing $Method $Url..." -NoNewline
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Body ($Body | ConvertTo-Json -Depth 10) -ContentType "application/json" -Headers $Headers
        } else {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $Headers
        }
        Write-Host " [OK]" -ForegroundColor Green
        return $response
    } catch {
        Write-Host " [FAILED]" -ForegroundColor Red
        Write-Host $_.Exception.Message
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader $_.Exception.Response.GetResponseStream()
            Write-Host $reader.ReadToEnd()
        }
        return $null
    }
}

# 1. Health Check
Write-Host "`n=== 1. Health Check ===" -ForegroundColor Cyan
Test-Endpoint "http://localhost:8002/health"

# 2. Create Center
Write-Host "`n=== 2. Create Center ===" -ForegroundColor Cyan
$center = @{
    name = "Test Center 1"
    code = "TC001"
    latitude = 16.0544
    longitude = 108.2022
    address = "Da Nang, Vietnam"
    total_capacity = 100
    is_public = $true
}
$createdCenter = Test-Endpoint "http://localhost:8002/api/v1/centers/" -Method "POST" -Body $center

if ($createdCenter) {
    $centerId = $createdCenter.id
    Write-Host "Created Center ID: $centerId" -ForegroundColor Yellow
    
    # 3. Get Center
    Write-Host "`n=== 3. Get Center ===" -ForegroundColor Cyan
    Test-Endpoint "http://localhost:8002/api/v1/centers/$centerId"
    
    # 4. Create Resource
    Write-Host "`n=== 4. Create Resource ===" -ForegroundColor Cyan
    $resource = @{
        name = "Water Bottles"
        type = "water"
        quantity = 500
        available_quantity = 500
        unit = "bottles"
        center_id = $centerId
    }
    Test-Endpoint "http://localhost:8002/api/v1/resources/" -Method "POST" -Body $resource
    
    # 5. Get Resources by Center
    Write-Host "`n=== 5. Get Resources by Center ===" -ForegroundColor Cyan
    Test-Endpoint "http://localhost:8002/api/v1/resources/center/$centerId"
    
    # 6. Test Nearby
    Write-Host "`n=== 6. Test Nearby Search ===" -ForegroundColor Cyan
    Test-Endpoint "http://localhost:8002/api/v1/centers/nearby?latitude=16.05&longitude=108.20&radius_km=10"
    
    # 7. Test Public Gateway API
    Write-Host "`n=== 7. Test Public Gateway API ===" -ForegroundColor Cyan
    Test-Endpoint "http://localhost:8000/api/open-data/centers"
}
