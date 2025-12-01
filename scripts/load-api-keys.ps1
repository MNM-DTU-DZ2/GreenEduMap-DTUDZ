# PowerShell script to load API keys into environment

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$apiKeysFile = Join-Path $scriptDir "api-keys.env"

if (Test-Path $apiKeysFile) {
    Write-Host "Loading API keys..." -ForegroundColor Cyan
    
    Get-Content $apiKeysFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.+)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
            Write-Host "✅ $name is set" -ForegroundColor Green
        }
    }
    
    Write-Host "`n✅ API keys loaded successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ api-keys.env not found!" -ForegroundColor Red
    exit 1
}
