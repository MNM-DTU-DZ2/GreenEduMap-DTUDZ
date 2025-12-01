$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Test-Endpoint {
    param($Url, $Method = "GET", $Body = $null)
    Write-Host "Testing $Method $Url..." -NoNewline
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Body ($Body | ConvertTo-Json -Depth 10) -ContentType "application/json"
        }
        else {
            $response = Invoke-RestMethod -Uri $Url -Method $Method
        }
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
    $initialScore = $bms.green_score
    
    $course = @{
        school_id      = $schoolId
        title          = "Recycling 101"
        description    = "Basic recycling"
        category       = "recycling"
        max_students   = 40
        duration_weeks = 12
        is_public      = $true
    }
    
    Test-Endpoint "http://localhost:8008/api/v1/green-courses" -Method "POST" -Body $course
    
    $updatedSchool = Test-Endpoint "http://localhost:8008/api/v1/schools/$schoolId"
    Write-Host "  Old Score: $initialScore" -ForegroundColor Yellow
    Write-Host "  New Score: $($updatedSchool.green_score)" -ForegroundColor Yellow
    
    if ($updatedSchool.green_score -gt $initialScore) {
        Write-Host "  [SUCCESS] Score increased after adding course" -ForegroundColor Green
    }
    else {
        Write-Host "  [FAILURE] Score did not increase" -ForegroundColor Red
    }
}

# 3. Test Manual Recalculation
if ($importResult) {
    Write-Host "`n=== 3. Test Manual Recalculation ===" -ForegroundColor Cyan
    $schoolId = $importResult.ids[0]
    Test-Endpoint "http://localhost:8008/api/v1/schools/$schoolId/calculate-score" -Method "POST"
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Green Score Tests Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green
