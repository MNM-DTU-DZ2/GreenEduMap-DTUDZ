# GreenEduMap - Git Quick Push v3.0 (PowerShell)
# Fast commit + push with conventional commits

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

function Write-Color {
    param(
        [string]$Text,
        [string]$Color = "White",
        [switch]$NoNewline
    )
    if ($NoNewline) {
        Write-Host $Text -ForegroundColor $Color -NoNewline
    }
    else {
        Write-Host $Text -ForegroundColor $Color
    }
}

function Write-Box {
    param([string]$Text, [string]$Color = "Cyan")
    Write-Color "=========================================================" $Color
    Write-Color "  $Text" $Color
    Write-Color "=========================================================" $Color
}

Clear-Host
Write-Host ""
Write-Box "GreenEduMap - Git Quick Push v3.0" "Cyan"
Write-Color "  Fast commit + push with conventional commits" "Gray"
Write-Box "" "Cyan"
Write-Host ""

# Check if in git repo
try {
    git rev-parse --git-dir 2>&1 | Out-Null
    $gitRoot = git rev-parse --show-toplevel
    Set-Location $gitRoot
}
catch {
    Write-Color "[ERROR] Not a git repository" "Red"
    Read-Host "Press Enter to exit"
    exit 1
}

# Get current branch
$currentBranch = git branch --show-current
Write-Color "Current branch: " "White" -NoNewline
Write-Color $currentBranch "Green"
Write-Host ""

# Check for changes
$null = git diff-index --quiet HEAD -- 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Color "[WARNING] No changes to commit!" "Yellow"
    Read-Host "Press Enter to exit"
    exit 0
}

Write-Color "Changed files:" "Yellow"
git status --short
Write-Host ""
Write-Color "=========================================================" "Cyan"

# STEP 1: Commit Type
Write-Host ""
Write-Color "STEP 1: Select Commit Type" "Cyan"
Write-Color "---------------------------------------------------------" "DarkGray"
Write-Host "  1) feat      - New feature"
Write-Host "  2) fix       - Bug fix"
Write-Host "  3) docs      - Documentation"
Write-Host "  4) style     - Code style"
Write-Host "  5) refactor  - Code refactoring"
Write-Host "  6) perf      - Performance"
Write-Host "  7) test      - Tests"
Write-Host "  8) build     - Build system"
Write-Host "  9) ci        - CI/CD"
Write-Host " 10) chore     - Maintenance"
Write-Host ""

$typeChoice = Read-Host "Select [1-10]"

$typeMap = @{
    "1"  = "feat"
    "2"  = "fix"
    "3"  = "docs"
    "4"  = "style"
    "5"  = "refactor"
    "6"  = "perf"
    "7"  = "test"
    "8"  = "build"
    "9"  = "ci"
    "10" = "chore"
}

if (-not $typeMap.ContainsKey($typeChoice)) {
    Write-Color "[ERROR] Invalid choice!" "Red"
    Read-Host "Press Enter to exit"
    exit 1
}

$type = $typeMap[$typeChoice]
Write-Color "[OK] Selected: $type" "Green"
Write-Host ""

# STEP 2: Scope
Write-Color "=========================================================" "Cyan"
Write-Color "STEP 2: Scope (Optional)" "Cyan"
Write-Color "---------------------------------------------------------" "DarkGray"
Write-Color "Examples: auth, api, docker, environment, resource, ai" "Gray"

$scope = Read-Host "Scope (press Enter to skip)"

if ($scope) {
    Write-Color "[OK] Scope: $scope" "Green"
}
else {
    Write-Color "No scope" "Gray"
}
Write-Host ""

# STEP 3: Commit Message
Write-Color "=========================================================" "Cyan"
Write-Color "STEP 3: Commit Message" "Cyan"
Write-Color "---------------------------------------------------------" "DarkGray"
Write-Color "Short description (imperative mood):" "White"
Write-Color 'Example: "add weather API endpoint" NOT "added..."' "Gray"

$message = Read-Host "> "

if (-not $message) {
    Write-Color "[ERROR] Message cannot be empty!" "Red"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Color "[OK] Message: $message" "Green"
Write-Host ""

# STEP 4: Optional Body
Write-Color "=========================================================" "Cyan"
Write-Color "STEP 4: Detailed Description (Optional)" "Cyan"
Write-Color "---------------------------------------------------------" "DarkGray"
Write-Color "PASTE your full message here (Ctrl+V), then press Enter TWICE to finish" "Yellow"
Write-Color "TIP: You can paste multi-line text with bullet points (-)!" "Gray"
Write-Host ""

$bodyLines = @()
$emptyLineCount = 0

while ($true) {
    try {
        $line = [Console]::ReadLine()
        if (-not $line) {
            $emptyLineCount++
            if ($emptyLineCount -ge 2) { break }  # Two consecutive empty lines = done
        }
        else {
            $emptyLineCount = 0
            $bodyLines += $line
        }
    }
    catch {
        break
    }
}

$body = ""
if ($bodyLines.Count -gt 0) {
    $body = $bodyLines -join "`n"
    Write-Color "[OK] Body added ($($bodyLines.Count) lines)" "Green"
}
else {
    Write-Color "No body text added" "Gray"
}
Write-Host ""

# STEP 5: Breaking Change
Write-Color "=========================================================" "Cyan"
Write-Color "STEP 5: Breaking Change?" "Cyan"
Write-Color "---------------------------------------------------------" "DarkGray"

$isBreaking = Read-Host "Is this a BREAKING CHANGE? [y/N]"

$breakingText = ""
if ($isBreaking -match "^[Yy]$") {
    Write-Color "[WARNING] Describe the breaking change:" "Yellow"
    Write-Color "Enter multiple lines. Press Enter on empty line to finish." "Gray"
    
    $breakingLines = @()
    $lineNum = 1
    
    while ($true) {
        $line = Read-Host "Line $lineNum"
        if (-not $line) { break }
        $breakingLines += $line
        $lineNum++
    }
    
    if ($breakingLines.Count -gt 0) {
        $breakingText = "BREAKING CHANGE: " + ($breakingLines -join "`n")
        Write-Color "[OK] Breaking change noted" "Green"
    }
}
Write-Host ""

# Build commit message
$commitHeader = if ($scope) {
    if ($isBreaking -match "^[Yy]$") {
        "${type}(${scope})!: ${message}"
    }
    else {
        "${type}(${scope}): ${message}"
    }
}
else {
    if ($isBreaking -match "^[Yy]$") {
        "${type}!: ${message}"
    }
    else {
        "${type}: ${message}"
    }
}

# Build full message
$fullMessage = $commitHeader

if ($body) {
    $fullMessage += "`n`n$body"
}

if ($breakingText) {
    $fullMessage += "`n`n$breakingText"
}

# Preview
Write-Color "=========================================================" "Cyan"
Write-Color "PREVIEW" "Cyan"
Write-Color "=========================================================" "Cyan"
Write-Color $fullMessage "Yellow"
Write-Color "=========================================================" "Cyan"
Write-Host ""

$confirm = Read-Host "Continue? [Y/n]"

if ($confirm -match "^[Nn]$") {
    Write-Color "Cancelled" "Yellow"
    Read-Host "Press Enter to exit"
    exit 0
}

# Execute
Write-Host ""
Write-Color "---------------------------------------------------------" "Cyan"
Write-Color "Executing..." "Cyan"
Write-Color "---------------------------------------------------------" "Cyan"

try {
    Write-Color "[1/3] Adding files..." "White"
    git add .
    
    Write-Color "[2/3] Committing..." "White"
    
    # Create temp file for commit message (No BOM)
    $tempFile = [System.IO.Path]::GetTempFileName()
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($tempFile, $fullMessage, $utf8NoBom)
    
    git commit -F $tempFile
    Remove-Item $tempFile
    
    if ($LASTEXITCODE -ne 0) {
        throw "Commit failed"
    }
    
    Write-Color "[2.5/3] Pulling latest changes..." "White"
    git pull origin $currentBranch
    
    if ($LASTEXITCODE -ne 0) {
        Write-Color "[ERROR] Pull failed! You may have conflicts." "Red"
        throw "Pull failed"
    }

    Write-Color "[3/3] Pushing to $currentBranch..." "White"
    git push origin $currentBranch
    
    if ($LASTEXITCODE -ne 0) {
        throw "Push failed"
    }
    
    Write-Host ""
    Write-Color "=========================================================" "Green"
    Write-Color "[SUCCESS]" "Green"
    Write-Color "=========================================================" "Green"
    Write-Color "Branch: " "White" -NoNewline
    Write-Color $currentBranch "Green"
    Write-Color "Commit: " "White" -NoNewline
    Write-Color $commitHeader "Green"
    
    if ($isBreaking -match "^[Yy]$") {
        Write-Color "[WARNING] BREAKING CHANGE committed" "Yellow"
    }
    
    # Optional: Merge to develop
    if ($currentBranch -ne "develop" -and $currentBranch -ne "main" -and $currentBranch -ne "master") {
        Write-Host ""
        Write-Color "=========================================================" "Cyan"
        $mergeDevelop = Read-Host "Merge into develop? [Y/n]"
        
        if ($mergeDevelop -notmatch "^[Nn]$") {
            Write-Host ""
            Write-Color "Merging into develop..." "Cyan"
            
            git checkout develop
            git pull origin develop
            git merge $currentBranch --no-edit
            
            if ($LASTEXITCODE -eq 0) {
                Write-Color "[OK] Merge successful!" "Green"
                git push origin develop
                Write-Color "[OK] Pushed develop" "Green"
                
                Write-Host ""
                Write-Color "Returning to $currentBranch..." "Cyan"
                git checkout $currentBranch
                
                Write-Host ""
                Write-Color "=========================================================" "Green"
                Write-Color "[SUCCESS] ALL DONE!" "Green"
                Write-Color "=========================================================" "Green"
                Write-Color "Pushed to: " "White" -NoNewline
                Write-Color $currentBranch "Green"
                Write-Color "Merged to: " "White" -NoNewline
                Write-Color "develop" "Green"
            }
            else {
                Write-Color "[ERROR] Merge conflict! Resolve manually." "Red"
                Read-Host "Press Enter to exit"
                exit 1
            }
        }
        else {
            Write-Color "Skipped merge" "Gray"
        }
    }
    
    Write-Host ""
    Write-Color "[TIP] CHANGELOG auto-updates on GitHub when merged!" "Cyan"
    Write-Color "View: .github/workflows/changelog.yml" "Gray"
    Write-Host ""
    
}
catch {
    Write-Color "[ERROR] Error: $_" "Red"
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"
