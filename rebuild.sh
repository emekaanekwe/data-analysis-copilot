#!/bin/bash

# Rebuild Docker Container Script
# This stops, rebuilds, and restarts your container

echo "🔄 Rebuilding Data Analysis Copilot..."
echo ""

# Detect docker compose command (V1 vs V2)
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "❌ Error: Docker Compose not found!"
    echo "   Please install Docker Compose and try again."
    exit 1
fi

echo "Using: $DOCKER_COMPOSE"
echo ""

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker stop $(docker ps -aq --filter "ancestor=streamlit_app") 2>/dev/null || true
docker stop data-analysis-copilot 2>/dev/null || true

# Remove existing containers
echo "🗑️  Removing old containers..."
docker rm $(docker ps -aq --filter "ancestor=streamlit_app") 2>/dev/null || true
docker rm data-analysis-copilot 2>/dev/null || true

# Ask user which method to use
echo ""
echo "Choose rebuild method:"
echo "1) Docker Compose (recommended - with live reloading)"
echo "2) Docker Build (your current method)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "🔨 Building with Docker Compose..."
    $DOCKER_COMPOSE down 2>/dev/null
    $DOCKER_COMPOSE up --build -d

    echo ""
    echo "✅ Container rebuilt and started!"
    echo "📊 Access at: http://localhost:8501"
    echo ""
    echo "View logs: $DOCKER_COMPOSE logs -f"
    echo ""
    $DOCKER_COMPOSE logs -f

elif [ "$choice" == "2" ]; then
    echo ""
    echo "🔨 Rebuilding image..."
    docker build -t streamlit_app .

    echo ""
    echo "▶️  Starting container with volume mounting..."
    docker run -d \
      --name data-analysis-copilot \
      -p 8501:8501 \
      -v $(pwd):/data-analysis-copilot \
      --env-file .env \
      streamlit_app

    echo ""
    echo "✅ Container rebuilt and started!"
    echo "📊 Access at: http://localhost:8501"
    echo ""
    echo "View logs: docker logs -f data-analysis-copilot"
    echo ""
    docker logs -f data-analysis-copilot
else
    echo "Invalid choice. Exiting."
    exit 1
fi
