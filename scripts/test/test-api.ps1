# Simple API Test Script for GreenEduMap
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " GreenEduMap API Quick Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$API = "http://localhost:8000"

# Test 1: Health Check
Write-Host "`n[1/5] Health Check..." -ForegroundColor Yellow
try {
    $r = Invoke-RestMethod "$API/health"
    Write-Host "✅ PASS - Gateway healthy" -ForegroundColor Green
}
catch {
    Write-Host "❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: List Schools
Write-Host "`n[2/5] List Schools..." -ForegroundColor Yellow
try {
    $schools = Invoke-RestMethod "$API/api/v1/schools?limit=3"
    Write-Host "✅ PASS - Found $($schools.Count) schools" -ForegroundColor Green
}
catch {
    Write-Host "❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Auth Register
Write-Host "`n[3/5] Auth Register..." -ForegroundColor Yellow
try {
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
    $body = @{
        username = "test$timestamp"
        email    = "test$timestamp@example.com"
        password = "password123"
    } | ConvertTo-Json
    
    $user = Invoke-RestMethod -Uri "$API/api/v1/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "✅ PASS - User created: $($user.username)" -ForegroundColor Green
    $global:testEmail = "test$timestamp@example.com"
    $global:testPass = "password123"
}
catch {
    Write-Host "❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Auth Login
Write-Host "`n[4/5] Auth Login..." -ForegroundColor Yellow
try {
    if ($global:testEmail) {
        $body = @{
            email    = $global:testEmail
            password = $global:testPass
        } | ConvertTo-Json
        
        $result = Invoke-RestMethod -Uri "$API/api/v1/auth/login" `
            -Method POST `
            -ContentType "application/json" `
            -Body $body
        
        Write-Host "✅ PASS - Login successful, got token" -ForegroundColor Green
        $global:token = $result.access_token
    }
    else {
        Write-Host "⚠️ SKIP - No test user" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Get Current User
Write-Host "`n[5/5] Get Current User..." -ForegroundColor Yellow
try {
    if ($global:token) {
        $headers = @{ Authorization = "Bearer $($global:token)" }
        $me = Invoke-RestMethod -Uri "$API/api/v1/auth/me" `
            -Headers $headers
        
        Write-Host "✅ PASS - Current user: $($me.username)" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️ SKIP - No token" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ FAIL - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " Test Complete!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan
