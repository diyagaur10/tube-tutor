# TubeTutor - Complete Setup Guide

## 🚀 Quick Start (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd teach-tube
```

### 2. Configure Environment
```bash
# Copy environment files
cp backend/env.example backend/.env
cp frontend/env.example frontend/.env

# Edit backend/.env and add your OpenAI API key:
# OPENAI_API_KEY=your_openai_api_key_here
# JWT_SECRET_KEY=your_random_secret_key_here
```

### 3. Start the Application

**On Linux/Mac:**
```bash
./start.sh
```

**On Windows:**
```bash
start.bat
```

**Or manually:**
```bash
docker-compose up -d
docker-compose exec backend python create_admin.py
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Login as Admin
- Email: `admin@tubetutor.com`
- Password: `admin123`

## 🔧 Manual Setup (Development)

### Backend Setup

1. **Install Python Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup Database**
```bash
# Install PostgreSQL and create database
createdb tubetutor

# Run migrations
alembic upgrade head
```

3. **Create Admin User**
```bash
python create_admin.py
```

4. **Start Backend**
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Start Development Server**
```bash
npm run dev
```

## 📱 Using the Application

### For Students
1. Register a new account or login
2. Browse videos on the home page
3. Click "Start Learning" on any video
4. Watch the video - it will pause at configured timestamps
5. Answer AI-generated questions to continue
6. Complete all questions to finish the video

### For Admins
1. Login with admin credentials
2. Go to Admin Dashboard
3. Upload videos with configured question timestamps
4. Questions are automatically generated using AI

## 🛠️ Development

### Project Structure
```
teach-tube/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic
│   │   └── auth.py        # Authentication
│   ├── alembic/          # Database migrations
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/       # Custom hooks
│   │   └── services/    # API services
│   └── package.json     # Node dependencies
└── docker-compose.yml   # Docker configuration
```

### Key Features Implemented

#### Backend Features
- ✅ JWT Authentication with bcrypt password hashing
- ✅ User roles (Admin/Student)
- ✅ Video upload and management
- ✅ AI question generation using OpenAI GPT-3.5-turbo
- ✅ Answer grading and retry logic
- ✅ Progress tracking
- ✅ Database models for Users, Videos, Questions, Progress
- ✅ RESTful API endpoints
- ✅ CORS configuration
- ✅ File upload handling

#### Frontend Features
- ✅ React with Vite and Tailwind CSS
- ✅ JWT authentication flow
- ✅ Video player with timestamp-based question triggering
- ✅ Question modal with different question types (MCQ, fill-in, one-word)
- ✅ Progress tracking and visualization
- ✅ Admin dashboard for video upload
- ✅ Responsive design
- ✅ Error handling and user feedback

#### Video Player Features
- ✅ Automatic pause at configured timestamps
- ✅ Question modal overlay
- ✅ Forward seeking prevention past incomplete questions
- ✅ Automatic rewind on failed questions
- ✅ Retry logic with limited attempts
- ✅ Progress visualization
- ✅ Real-time timestamp tracking

### API Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

#### Videos
- `GET /videos/` - List all published videos
- `GET /videos/{id}` - Get video details
- `POST /videos/upload` - Upload new video (Admin only)
- `GET /videos/{id}/questions` - Get video questions

#### Questions
- `POST /questions/{id}/answer` - Submit answer to question

#### Progress
- `GET /progress/{video_id}` - Get user progress for video
- `PUT /progress/{video_id}` - Update user progress

### Database Schema

#### Users Table
- id, email, username, hashed_password, is_admin, created_at

#### Videos Table
- id, title, description, video_url, thumbnail_url, duration, transcript, is_published, uploader_id, created_at

#### Questions Table
- id, video_id, timestamp, question_type, question_text, options, correct_answer, explanation, retry_limit, rewind_seconds, is_final_quiz

#### User Progress Table
- id, user_id, video_id, current_timestamp, completed_questions, failed_attempts, is_completed, final_score, last_updated

## 🚀 Deployment

### Frontend (Vercel)
1. Connect GitHub repository to Vercel
2. Set environment variables:
   - `VITE_API_URL`: Your backend URL
3. Deploy

### Backend (Render/Railway)
1. Connect GitHub repository
2. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `JWT_SECRET_KEY`: Random secret key
   - `CORS_ORIGINS`: Your frontend URL
3. Deploy

## 🔍 Troubleshooting

### Common Issues

1. **Docker not starting**
   - Ensure Docker Desktop is running
   - Check if ports 3000, 8000, 5432 are available

2. **Database connection errors**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in backend/.env

3. **OpenAI API errors**
   - Verify OPENAI_API_KEY is set correctly
   - Check API key has sufficient credits

4. **Frontend not loading**
   - Check VITE_API_URL in frontend/.env
   - Ensure backend is running on correct port

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/tubetutor
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=TubeTutor
```

## 🎯 Next Steps

1. **Add more question types** (drag-and-drop, image-based)
2. **Implement video transcription** using Whisper
3. **Add analytics dashboard** for learning progress
4. **Implement video chapters** and navigation
5. **Add social features** (comments, ratings)
6. **Mobile app** using React Native
7. **Advanced AI features** (personalized learning paths)

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Ensure all environment variables are set correctly
4. Verify Docker and all services are running properly

Happy learning with TubeTutor! 🎓
