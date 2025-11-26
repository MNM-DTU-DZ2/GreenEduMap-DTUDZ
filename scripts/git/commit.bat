@echo off
REM GreenEduMap Conventional Commit Script
REM Supports: Windows
REM Usage: scripts\git\commit.bat

setlocal enabledelayedexpansion

REM Colors (Windows doesn't support ANSI by default, but works on newer versions)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "MAGENTA=[95m"
set "CYAN=[96m"
set "NC=[0m"

cls
echo %CYAN%=========================================================%NC%
echo %CYAN%        GreenEduMap Commit Helper v1.0                 %NC%
echo %CYAN%        Conventional Commits + Auto CHANGELOG           %NC%
echo %CYAN%=========================================================%NC%
echo.

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo %RED%Error: Not a git repository%NC%
    exit /b 1
)

REM Get current branch
for /f "tokens=*" %%i in ('git branch --show-current') do set CURRENT_BRANCH=%%i
echo %BLUE%Current branch:%NC% %GREEN%!CURRENT_BRANCH!%NC%
echo.

REM Check for uncommitted changes
git diff-index --quiet HEAD -- >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%You have uncommitted changes.%NC%
    echo.
) else (
    echo %RED%No changes to commit!%NC%
    exit /b 0
)

REM ============================================
REM STEP 1: Select Commit Type
REM ============================================
echo %CYAN%=========================================================%NC%
echo %CYAN% STEP 1: Select Commit Type (Conventional Commits)     %NC%
echo %CYAN%=========================================================%NC%
echo.
echo   1) feat      - New feature
echo   2) fix       - Bug fix
echo   3) docs      - Documentation changes
echo   4) style     - Code style changes (formatting, etc.)
echo   5) refactor  - Code refactoring
echo   6) perf      - Performance improvements
echo   7) test      - Adding tests
echo   8) build     - Build system changes
echo   9) ci        - CI/CD changes
echo  10) chore     - Other changes (maintenance)
echo  11) revert    - Revert previous commit
echo.
set /p TYPE_CHOICE="Select commit type [1-11]: "

if "%TYPE_CHOICE%"=="1" set COMMIT_TYPE=feat
if "%TYPE_CHOICE%"=="2" set COMMIT_TYPE=fix
if "%TYPE_CHOICE%"=="3" set COMMIT_TYPE=docs
if "%TYPE_CHOICE%"=="4" set COMMIT_TYPE=style
if "%TYPE_CHOICE%"=="5" set COMMIT_TYPE=refactor
if "%TYPE_CHOICE%"=="6" set COMMIT_TYPE=perf
if "%TYPE_CHOICE%"=="7" set COMMIT_TYPE=test
if "%TYPE_CHOICE%"=="8" set COMMIT_TYPE=build
if "%TYPE_CHOICE%"=="9" set COMMIT_TYPE=ci
if "%TYPE_CHOICE%"=="10" set COMMIT_TYPE=chore
if "%TYPE_CHOICE%"=="11" set COMMIT_TYPE=revert

if not defined COMMIT_TYPE (
    echo %RED%Invalid choice!%NC%
    exit /b 1
)

echo %GREEN%Selected: !COMMIT_TYPE!%NC%
echo.

REM ============================================
REM STEP 2: Scope (Optional)
REM ============================================
echo %CYAN%=========================================================%NC%
echo %CYAN% STEP 2: Scope (Optional)                              %NC%
echo %CYAN%=========================================================%NC%
echo.
echo Examples: api, frontend, backend, auth, database, ci, etc.
set /p SCOPE="Enter scope (press Enter to skip): "

if defined SCOPE (
    set SCOPE_TEXT=(!SCOPE!)
    echo %GREEN%Scope: !SCOPE!%NC%
) else (
    set SCOPE_TEXT=
    echo %YELLOW%No scope%NC%
)
echo.

REM ============================================
REM STEP 3: Commit Message
REM ============================================
echo %CYAN%=========================================================%NC%
echo %CYAN% STEP 3: Commit Message                                %NC%
echo %CYAN%=========================================================%NC%
echo.
echo Enter a short, descriptive message (imperative mood)
echo Example: 'add user authentication' NOT 'added user authentication'
set /p MESSAGE="Message: "

if not defined MESSAGE (
    echo %RED%Error: Message cannot be empty!%NC%
    exit /b 1
)

echo %GREEN%Message: !MESSAGE!%NC%
echo.

REM ============================================
REM STEP 4: Breaking Change?
REM ============================================
echo %CYAN%=========================================================%NC%
echo %CYAN% STEP 4: Is this a breaking change?                    %NC%
echo %CYAN%=========================================================%NC%
echo.
set /p BREAKING="Breaking change? (y/N): "

set BREAKING_TEXT=
if /i "!BREAKING!"=="y" (
    set BREAKING_TEXT=!
    echo %RED%Breaking change marked!%NC%
) else (
    echo %GREEN%Not a breaking change%NC%
)
echo.

REM ============================================
REM STEP 5: Preview & Confirm
REM ============================================
set FULL_MESSAGE=!COMMIT_TYPE!!SCOPE_TEXT!!BREAKING_TEXT!: !MESSAGE!

echo %CYAN%=========================================================%NC%
echo %CYAN% Preview                                                %NC%
echo %CYAN%=========================================================%NC%
echo.
echo %MAGENTA%Commit message:%NC%
echo %GREEN%  !FULL_MESSAGE!%NC%
echo.
echo %YELLOW%Files to be committed:%NC%
git status --short
echo.

set /p CONFIRM="Continue? (Y/n): "
if /i "!CONFIRM!"=="n" (
    echo %RED%Aborted!%NC%
    exit /b 0
)

REM ============================================
REM STEP 6: Commit
REM ============================================
echo.
echo %BLUE%Committing...%NC%

git add .
git commit -m "!FULL_MESSAGE!"

if errorlevel 1 (
    echo %RED%Commit failed!%NC%
    exit /b 1
)

echo %GREEN%Committed successfully!%NC%
echo.

REM ============================================
REM STEP 7: Push to current branch
REM ============================================
echo %CYAN%=========================================================%NC%
echo %CYAN% STEP 7: Push to Remote                                 %NC%
echo %CYAN%=========================================================%NC%
echo.

set /p PUSH_CONFIRM="Push to origin/!CURRENT_BRANCH!? (Y/n): "
if /i not "!PUSH_CONFIRM!"=="n" (
    echo %BLUE%Pushing to origin/!CURRENT_BRANCH!...%NC%
    git push origin !CURRENT_BRANCH!
    echo %GREEN%Pushed successfully!%NC%
) else (
    echo %YELLOW%Skipped push%NC%
)
echo.

REM ============================================
REM STEP 8: Merge to develop?
REM ============================================
if not "!CURRENT_BRANCH!"=="develop" if not "!CURRENT_BRANCH!"=="main" (
    echo %CYAN%=========================================================%NC%
    echo %CYAN% STEP 8: Merge to Develop                              %NC%
    echo %CYAN%=========================================================%NC%
    echo.
    
    set /p MERGE_CONFIRM="Merge !CURRENT_BRANCH! into develop? (Y/n): "
    if /i not "!MERGE_CONFIRM!"=="n" (
        echo %BLUE%Merging into develop...%NC%
        
        set FEATURE_BRANCH=!CURRENT_BRANCH!
        
        REM Checkout to develop
        git checkout develop 2>nul || git checkout -b develop
        
        REM Pull latest
        git pull origin develop 2>nul
        
        REM Merge feature branch
        git merge !FEATURE_BRANCH! --no-ff -m "Merge branch '!FEATURE_BRANCH!' into develop"
        
        echo %GREEN%Merged successfully!%NC%
        echo.
        
        REM Push develop
        set /p PUSH_DEVELOP="Push develop to remote? (Y/n): "
        if /i not "!PUSH_DEVELOP!"=="n" (
            git push origin develop
            echo %GREEN%Pushed develop!%NC%
        )
        
        REM Return to feature branch
        echo.
        set /p RETURN="Return to !FEATURE_BRANCH!? (Y/n): "
        if /i not "!RETURN!"=="n" (
            git checkout !FEATURE_BRANCH!
            echo %GREEN%Returned to !FEATURE_BRANCH!%NC%
        )
    ) else (
        echo %YELLOW%Skipped merge%NC%
    )
)

REM ============================================
REM STEP 9: Generate CHANGELOG
REM ============================================
echo.
echo %CYAN%=========================================================%NC%
echo %CYAN% STEP 9: Update CHANGELOG                               %NC%
echo %CYAN%=========================================================%NC%
echo.

where conventional-changelog >nul 2>&1
if %errorlevel% equ 0 (
    echo %BLUE%Generating CHANGELOG...%NC%
    conventional-changelog -p angular -i CHANGELOG.md -s
    echo %GREEN%CHANGELOG updated!%NC%
) else (
    where git-cliff >nul 2>&1
    if %errorlevel% equ 0 (
        echo %BLUE%Generating CHANGELOG with git-cliff...%NC%
        git-cliff -o CHANGELOG.md
        echo %GREEN%CHANGELOG updated!%NC%
    ) else (
        echo %YELLOW%No CHANGELOG generator found!%NC%
        echo %YELLOW%Install: npm install -g conventional-changelog-cli%NC%
        echo %YELLOW%Or: cargo install git-cliff%NC%
    )
)

echo.
echo %GREEN%=========================================================%NC%
echo %GREEN%                 ALL DONE!                             %NC%
echo %GREEN%=========================================================%NC%
echo.
echo %CYAN%Summary:%NC%
echo   Commit: %GREEN%!FULL_MESSAGE!%NC%
echo   Branch: %GREEN%!CURRENT_BRANCH!%NC%
echo.

pause
