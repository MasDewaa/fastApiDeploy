#!/bin/bash

echo "🚀 Running Batik Classification API with Docker Compose..."

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Installing..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start
echo "📦 Building and starting containers..."
docker-compose up --build -d

# Wait for container to start
echo "⏳ Waiting for API to be ready..."
sleep 15

# Test the API
echo "🧪 Testing API..."
curl -f http://localhost:8000/health

if [ $? -eq 0 ]; then
    echo "✅ API is running successfully!"
    echo "🌐 API URL: http://localhost:8000"
    echo "📊 Health: http://localhost:8000/health"
    echo "📋 Model info: http://localhost:8000/model-info"
    echo "🔍 API docs: http://localhost:8000/docs"
    echo ""
    echo "📋 Commands:"
    echo "  View logs: docker-compose logs -f"
    echo "  Stop: docker-compose down"
    echo "  Restart: docker-compose restart"
else
    echo "❌ API failed to start!"
    echo "📋 Check logs: docker-compose logs"
fi 