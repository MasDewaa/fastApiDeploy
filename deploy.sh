#!/bin/bash

echo "🚀 Deploying Batik Classification API..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t batik-classification-api .

# Stop existing container if running
echo "🛑 Stopping existing container..."
docker stop batik-api 2>/dev/null || true
docker rm batik-api 2>/dev/null || true

# Run new container
echo "▶️ Starting container..."
docker run -d \
  --name batik-api \
  -p 8000:8000 \
  --restart unless-stopped \
  batik-classification-api

# Wait for container to start
echo "⏳ Waiting for API to be ready..."
sleep 10

# Test the API
echo "🧪 Testing API..."
curl -f http://localhost:8000/health

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 API is running at: http://localhost:8000"
    echo "📊 Health check: http://localhost:8000/health"
    echo "📋 Model info: http://localhost:8000/model-info"
    echo "🔍 API docs: http://localhost:8000/docs"
else
    echo "❌ Deployment failed!"
    echo "📋 Check logs: docker logs batik-api"
fi 