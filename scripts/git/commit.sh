#!/bin/bash

# GreenEduMap Conventional Commit Script
# Supports: macOS & Linux
# Usage: ./scripts/git/commit.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Header
clear
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          GreenEduMap Commit Helper v1.0              ║${NC}"
echo -e "${CYAN}║          Conventional Commits + Auto CHANGELOG        ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not a git repository${NC}"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}Current branch:${NC} ${GREEN}$CURRENT_BRANCH${NC}"
echo ""

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}You have uncommitted changes.${NC}"
    echo ""
else
    echo -e "${RED}No changes to commit!${NC}"
    exit 0
fi

# ============================================
# STEP 1: Select Commit Type
# ============================================
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║ STEP 1: Select Commit Type (Conventional Commits)   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo "  1) feat      - New feature"
echo "  2) fix       - Bug fix"
echo "  3) docs      - Documentation changes"
echo "  4) style     - Code style changes (formatting, etc.)"
echo "  5) refactor  - Code refactoring"
echo "  6) perf      - Performance improvements"
echo "  7) test      - Adding tests"
echo "  8) build     - Build system changes"
echo "  9) ci        - CI/CD changes"
echo " 10) chore     - Other changes (maintenance)"
echo " 11) revert    - Revert previous commit"
echo ""
read -p "Select commit type [1-11]: " TYPE_CHOICE

case $TYPE_CHOICE in
    1) COMMIT_TYPE="feat" ;;
    2) COMMIT_TYPE="fix" ;;
    3) COMMIT_TYPE="docs" ;;
    4) COMMIT_TYPE="style" ;;
    5) COMMIT_TYPE="refactor" ;;
    6) COMMIT_TYPE="perf" ;;
    7) COMMIT_TYPE="test" ;;
    8) COMMIT_TYPE="build" ;;
    9) COMMIT_TYPE="ci" ;;
    10) COMMIT_TYPE="chore" ;;
    11) COMMIT_TYPE="revert" ;;
    *) 
        echo -e "${RED}Invalid choice!${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}✓ Selected: ${COMMIT_TYPE}${NC}"
echo ""

# ============================================
# STEP 2: Scope (Optional)
# ============================================
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║ STEP 2: Scope (Optional)                             ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Examples: api, frontend, backend, auth, database, ci, etc."
read -p "Enter scope (press Enter to skip): " SCOPE

if [ -n "$SCOPE" ]; then
    SCOPE_TEXT="($SCOPE)"
    echo -e "${GREEN}✓ Scope: ${SCOPE}${NC}"
else
    SCOPE_TEXT=""
    echo -e "${YELLOW}⊘ No scope${NC}"
fi
echo ""

# ============================================
# STEP 3: Commit Message
# ============================================
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║ STEP 3: Commit Message                               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Enter a short, descriptive message (imperative mood)"
echo "Example: 'add user authentication' NOT 'added user authentication'"
read -p "Message: " MESSAGE

if [ -z "$MESSAGE" ]; then
    echo -e "${RED}Error: Message cannot be empty!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Message: ${MESSAGE}${NC}"
echo ""

# ============================================
# STEP 4: Breaking Change?
# ============================================
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║ STEP 4: Is this a breaking change?                   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
read -p "Breaking change? (y/N): " BREAKING

BREAKING_TEXT=""
if [[ $BREAKING =~ ^[Yy]$ ]]; then
    BREAKING_TEXT="!"
    echo -e "${RED}⚠ Breaking change marked!${NC}"
else
    echo -e "${GREEN}✓ Not a breaking change${NC}"
fi
echo ""

# ============================================
# STEP 5: Preview & Confirm
# ============================================
FULL_MESSAGE="${COMMIT_TYPE}${SCOPE_TEXT}${BREAKING_TEXT}: ${MESSAGE}"

echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║ Preview                                               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${MAGENTA}Commit message:${NC}"
echo -e "${GREEN}  $FULL_MESSAGE${NC}"
echo ""
echo -e "${YELLOW}Files to be committed:${NC}"
git status --short
echo ""

read -p "Continue? (Y/n): " CONFIRM
if [[ $CONFIRM =~ ^[Nn]$ ]]; then
    echo -e "${RED}Aborted!${NC}"
    exit 0
fi

# ============================================
# STEP 6: Commit
# ============================================
echo ""
echo -e "${BLUE}⏳ Committing...${NC}"

git add .
git commit -m "$FULL_MESSAGE"

echo -e "${GREEN}✓ Committed successfully!${NC}"
echo ""

# ============================================
# STEP 7: Push to current branch
# ============================================
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║ STEP 7: Push to Remote                                ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

read -p "Push to origin/$CURRENT_BRANCH? (Y/n): " PUSH_CONFIRM
if [[ ! $PUSH_CONFIRM =~ ^[Nn]$ ]]; then
    echo -e "${BLUE}⏳ Pushing to origin/$CURRENT_BRANCH...${NC}"
    git push origin $CURRENT_BRANCH
    echo -e "${GREEN}✓ Pushed successfully!${NC}"
else
    echo -e "${YELLOW}⊘ Skipped push${NC}"
fi
echo ""

# ============================================
# STEP 8: Merge to develop?
# ============================================
if [ "$CURRENT_BRANCH" != "develop" ] && [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║ STEP 8: Merge to Develop                             ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    read -p "Merge $CURRENT_BRANCH into develop? (Y/n): " MERGE_CONFIRM
    if [[ ! $MERGE_CONFIRM =~ ^[Nn]$ ]]; then
        echo -e "${BLUE}⏳ Merging into develop...${NC}"
        
        # Save current branch
        FEATURE_BRANCH=$CURRENT_BRANCH
        
        # Checkout to develop
        git checkout develop 2>/dev/null || git checkout -b develop
        
        # Pull latest
        git pull origin develop 2>/dev/null || echo "First time on develop"
        
        # Merge feature branch
        git merge $FEATURE_BRANCH --no-ff -m "Merge branch '$FEATURE_BRANCH' into develop"
        
        echo -e "${GREEN}✓ Merged successfully!${NC}"
        echo ""
        
        # Push develop
        read -p "Push develop to remote? (Y/n): " PUSH_DEVELOP
        if [[ ! $PUSH_DEVELOP =~ ^[Nn]$ ]]; then
            git push origin develop
            echo -e "${GREEN}✓ Pushed develop!${NC}"
        fi
        
        # Return to feature branch
        echo ""
        read -p "Return to $FEATURE_BRANCH? (Y/n): " RETURN
        if [[ ! $RETURN =~ ^[Nn]$ ]]; then
            git checkout $FEATURE_BRANCH
            echo -e "${GREEN}✓ Returned to $FEATURE_BRANCH${NC}"
        fi
    else
        echo -e "${YELLOW}⊘ Skipped merge${NC}"
    fi
fi

# ============================================
# STEP 9: Generate CHANGELOG
# ============================================
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║ STEP 9: Update CHANGELOG                              ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

if command -v conventional-changelog &> /dev/null; then
    echo -e "${BLUE}⏳ Generating CHANGELOG...${NC}"
    conventional-changelog -p angular -i CHANGELOG.md -s
    echo -e "${GREEN}✓ CHANGELOG updated!${NC}"
elif command -v git-cliff &> /dev/null; then
    echo -e "${BLUE}⏳ Generating CHANGELOG with git-cliff...${NC}"
    git-cliff -o CHANGELOG.md
    echo -e "${GREEN}✓ CHANGELOG updated!${NC}"
else
    echo -e "${YELLOW}⚠ No CHANGELOG generator found!${NC}"
    echo -e "${YELLOW}Install: npm install -g conventional-changelog-cli${NC}"
    echo -e "${YELLOW}Or: cargo install git-cliff${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                 ✓ ALL DONE!                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Summary:${NC}"
echo -e "  Commit: ${GREEN}$FULL_MESSAGE${NC}"
echo -e "  Branch: ${GREEN}$CURRENT_BRANCH${NC}"
echo ""
