#!/bin/bash

# Stop the development container

# Detect docker compose command (V1 vs V2)
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "❌ Error: Docker Compose not found!"
    exit 1
fi

echo "🛑 Stopping Data Analysis Copilot container..."
$DOCKER_COMPOSE down

echo ""
echo "✅ Container stopped successfully!"
echo ""
echo "To start again, run: ./start-dev.sh"
