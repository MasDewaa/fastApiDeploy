#!/bin/bash

# 🎨 Batik Classification API Deployment Script
# Script untuk deploy aplikasi FastAPI dengan Docker

set -e  # Exit on any error

echo "🚀 Starting Batik Classification API Deployment..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Check if required files exist
check_files() {
    print_status "Checking required files..."
    
    required_files=("app.py" "requirements.txt" "Dockerfile" "mainModel.keras")
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Required file not found: $file"
            exit 1
        fi
    done
    
    print_success "All required files found"
}

# Stop existing container if running
stop_existing_container() {
    print_status "Checking for existing containers..."
    
    if docker ps -q -f name=batik-classification-api | grep -q .; then
        print_warning "Found existing container. Stopping it..."
        docker stop batik-classification-api
        docker rm batik-classification-api
        print_success "Existing container stopped and removed"
    fi
}

# Build Docker image
build_image() {
    print_status "Building Docker image..."
    
    if docker build -t batik-classification-api .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Run container
run_container() {
    print_status "Starting container..."
    
    if docker run -d \
        --name batik-classification-api \
        -p 8000:8000 \
        --restart unless-stopped \
        batik-classification-api; then
        print_success "Container started successfully"
    else
        print_error "Failed to start container"
        exit 1
    fi
}

# Wait for API to be ready
wait_for_api() {
    print_status "Waiting for API to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            print_success "API is ready!"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - API not ready yet..."
        sleep 2
        ((attempt++))
    done
    
    print_error "API failed to start within expected time"
    return 1
}

# Test API endpoints
test_api() {
    print_status "Testing API endpoints..."
    
    # Test health endpoint
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        print_success "Health endpoint working"
    else
        print_error "Health endpoint failed"
        return 1
    fi
    
    # Test root endpoint
    if curl -s http://localhost:8000/ | grep -q "Batik Classification API"; then
        print_success "Root endpoint working"
    else
        print_error "Root endpoint failed"
        return 1
    fi
    
    print_success "All API tests passed"
}

# Show container status
show_status() {
    print_status "Container status:"
    docker ps -f name=batik-classification-api
    
    echo ""
    print_status "API endpoints:"
    echo "  Health check: http://localhost:8000/health"
    echo "  API docs: http://localhost:8000/api-docs"
    echo "  Root endpoint: http://localhost:8000/"
    echo "  Prediction endpoint: http://localhost:8000/predict"
    echo ""
    print_status "Test the API:"
    echo "  curl http://localhost:8000/health"
    echo "  curl http://localhost:8000/model-info"
    echo ""
    print_status "View logs:"
    echo "  docker logs batik-classification-api"
    echo ""
    print_status "Stop container:"
    echo "  docker stop batik-classification-api"
}

# Main deployment function
main() {
    echo ""
    print_status "Starting deployment process..."
    
    check_docker
    check_files
    stop_existing_container
    build_image
    run_container
    
    echo ""
    print_status "Waiting for container to start..."
    sleep 5
    
    if wait_for_api; then
        test_api
        echo ""
        print_success "🎉 Deployment completed successfully!"
        show_status
    else
        print_error "❌ Deployment failed"
        echo ""
        print_status "Container logs:"
        docker logs batik-classification-api
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "stop")
        print_status "Stopping container..."
        docker stop batik-classification-api 2>/dev/null || true
        docker rm batik-classification-api 2>/dev/null || true
        print_success "Container stopped"
        ;;
    "logs")
        print_status "Showing container logs..."
        docker logs -f batik-classification-api
        ;;
    "restart")
        print_status "Restarting container..."
        docker restart batik-classification-api
        print_success "Container restarted"
        ;;
    "status")
        print_status "Container status:"
        docker ps -f name=batik-classification-api
        ;;
    "test")
        print_status "Testing API..."
        if curl -f http://localhost:8000/health &> /dev/null; then
            print_success "API is running"
            test_api
        else
            print_error "API is not running"
            exit 1
        fi
        ;;
    *)
        main
        ;;
esac 