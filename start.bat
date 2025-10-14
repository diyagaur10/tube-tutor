@echo off
echo 🚀 Starting TubeTutor...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if .env files exist
if not exist "backend\.env" (
    echo 📝 Creating backend\.env from template...
    copy backend\env.example backend\.env
    echo ⚠️  Please update backend\.env with your OpenAI API key and other settings
)

if not exist "frontend\.env" (
    echo 📝 Creating frontend\.env from template...
    copy frontend\env.example frontend\.env
)

REM Create uploads directory
if not exist "backend\uploads\videos" mkdir backend\uploads\videos

echo 🐳 Starting services with Docker Compose...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo 🔧 Setting up database and creating admin user...
docker-compose exec backend python create_admin.py

echo.
echo ✅ TubeTutor is now running!
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo 👤 Admin Login:
echo    Email: admin@tubetutor.com
echo    Password: admin123
echo.
echo To stop the application, run: docker-compose down
pause
