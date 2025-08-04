#!/bin/bash

echo "🚀 Deploying Batik Classification API to Server..."

# 1. Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker installed"
fi

# 2. Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# 3. Build Docker image
echo "📦 Building Docker image..."
docker build -t batik-classification-api .

# 4. Stop existing container if running
echo "🛑 Stopping existing container..."
docker stop batik-api 2>/dev/null || true
docker rm batik-api 2>/dev/null || true

# 5. Run new container
echo "▶️ Starting container..."
docker run -d \
  --name batik-api \
  -p 8000:8000 \
  --restart unless-stopped \
  batik-classification-api

# 6. Wait for container to start
echo "⏳ Waiting for API to be ready..."
sleep 15

# 7. Test the API
echo "🧪 Testing API..."
curl -f http://localhost:8000/health

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 API is running at: http://YOUR_SERVER_IP:8000"
    echo "📊 Health check: http://YOUR_SERVER_IP:8000/health"
    echo "📋 Model info: http://YOUR_SERVER_IP:8000/model-info"
    echo "🔍 API docs: http://YOUR_SERVER_IP:8000/docs"
else
    echo "❌ Deployment failed!"
    echo "📋 Check logs: docker logs batik-api"
fi 