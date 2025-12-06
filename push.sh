#!/bin/bash

# ShopManager - GitHub Push Script
# This script automatically stages, commits, and pushes changes to GitHub

echo "🚀 ShopManager - GitHub Push Script"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not a git repository${NC}"
    exit 1
fi

# Get the current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${YELLOW}📍 Current branch: ${GREEN}${BRANCH}${NC}"
echo ""

# Check for uncommitted changes
if git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}ℹ️  No changes to commit${NC}"
    exit 0
fi

echo -e "${YELLOW}📝 Changes detected. Staging all files...${NC}"

# Stage all changes
git add .

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error: Failed to stage files${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Files staged successfully${NC}"
echo ""

# Show staged changes
echo -e "${YELLOW}📋 Staged files:${NC}"
git diff --cached --name-only

echo ""
echo -e "${YELLOW}💬 Enter commit message (or press Enter for default):${NC}"
read -p "> " COMMIT_MESSAGE

# Use default message if empty
if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="🎨 ShopManager design enhancement - professional branding update"
fi

echo ""
echo -e "${YELLOW}🔄 Committing changes...${NC}"

# Commit changes
git commit -m "$COMMIT_MESSAGE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error: Failed to commit changes${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Changes committed successfully${NC}"
echo ""
echo -e "${YELLOW}🌐 Pushing to GitHub...${NC}"

# Push to GitHub
git push origin "$BRANCH"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error: Failed to push to GitHub${NC}"
    echo -e "${YELLOW}💡 Make sure you have push access and your remote is configured${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Push successful!${NC}"
echo -e "${GREEN}🎉 All changes have been pushed to ${BRANCH} on GitHub${NC}"
echo ""
