#!/bin/bash
# Setup script to load API keys into environment

# Load API keys from api-keys.env
if [ -f "$(dirname "$0")/api-keys.env" ]; then
    echo "Loading API keys..."
    export $(cat "$(dirname "$0")/api-keys.env" | grep -v '^#' | xargs)
    echo "✅ API keys loaded successfully!"
    echo "OPENWEATHER_API_KEY is set: ${OPENWEATHER_API_KEY:0:10}..."
else
    echo "❌ api-keys.env not found!"
    exit 1
fi
