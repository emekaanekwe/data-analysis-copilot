#!/bin/bash

# Development startup script for Data Analysis Copilot
# This script starts the Docker container with live reloading

echo "🚀 Starting Data Analysis Copilot in Development Mode..."
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

echo "✅ Using: $DOCKER_COMPOSE"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Creating .env template..."
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
    echo "   ✅ .env file created. Please add your OpenAI API key."
    echo ""
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "   Please start Docker Desktop and try again."
    exit 1
fi

# Stop any existing container
echo "🛑 Stopping existing containers..."
$DOCKER_COMPOSE down 2>/dev/null

# Build and start
echo "🔨 Building Docker image..."
$DOCKER_COMPOSE build

echo ""
echo "▶️  Starting container with live reloading..."
$DOCKER_COMPOSE up -d

echo ""
echo "✅ Container started successfully!"
echo ""
echo "📊 Access your app at: http://localhost:8501"
echo ""
echo "📝 Useful commands:"
echo "   View logs:        $DOCKER_COMPOSE logs -f"
echo "   Stop container:   $DOCKER_COMPOSE down"
echo "   Restart:          $DOCKER_COMPOSE restart"
echo "   Shell access:     docker exec -it data-analysis-copilot bash"
echo ""
echo "💡 Your changes will auto-reload in the browser!"
echo ""

# Follow logs
echo "Following logs (Ctrl+C to exit, container keeps running)..."
echo "-----------------------------------------------------------"
$DOCKER_COMPOSE logs -f
