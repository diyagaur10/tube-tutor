#!/bin/bash

# TubeTutor Startup Script

echo "🚀 Starting TubeTutor..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/env.example backend/.env
    echo "⚠️  Please update backend/.env with your OpenAI API key and other settings"
fi

if [ ! -f "frontend/.env" ]; then
    echo "📝 Creating frontend/.env from template..."
    cp frontend/env.example frontend/.env
fi

# Create uploads directory
mkdir -p backend/uploads/videos

echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔧 Setting up database and creating admin user..."
docker-compose exec backend python create_admin.py

echo ""
echo "✅ TubeTutor is now running!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "👤 Admin Login:"
echo "   Email: admin@tubetutor.com"
echo "   Password: admin123"
echo ""
echo "To stop the application, run: docker-compose down"
