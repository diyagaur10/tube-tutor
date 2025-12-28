# TubeTutor - Interactive Learning Platform

A YouTube-like learning platform where admins upload videos and students watch them with AI-generated questions at configured timestamps.

## Features

- **Interactive Video Learning**: Videos pause at configured timestamps to show AI-generated questions
- **Question Types**: Multiple choice, fill-in-the-blank, and one-word answer questions
- **Progress Tracking**: Students must answer correctly to continue, with limited retries
- **Smart Rewind**: Failed questions trigger video rewind with AI-generated summaries
- **Admin Dashboard**: Upload videos and configure question timestamps
- **JWT Authentication**: Secure user authentication and authorization

## Tech Stack

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: PostgreSQL + SQLAlchemy + Alembic
- **AI**: OpenAI Whisper (Local Transcription) & Google Gemini 1.5 Flash (Question Generation).
- **Authentication**: JWT tokens with bcrypt password hashing

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- PostgreSQL (if running locally)

### Environment Setup

1. Copy environment files:
```bash
cp backend/env.example backend/.env
cp frontend/env.example frontend/.env
```

2. Update `backend/.env` with your credentials:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/tubetutor
GEMENI_API_KEY=your_gemini_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```

### Running with Docker

1. Start all services:
```bash
docker-compose up -d
```

2. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Running Locally

#### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up database:
```bash
# Create database
createdb tubetutor

# Run migrations
alembic upgrade head
```

3. Start the server:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Usage

### For Students

1. Register/Login to the platform
2. Browse available videos on the home page
3. Click "Start Learning" on any video
4. Watch the video - it will pause at configured timestamps
5. Answer the AI-generated questions to continue
6. Complete all questions to finish the video

### For Admins

1. Login with admin credentials
2. Go to Admin Dashboard
3. Upload videos with configured question timestamps
4. Questions are automatically generated using AI based on video content

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

### Videos
- `GET /videos/` - List all published videos
- `GET /videos/{id}` - Get video details
- `POST /videos/upload` - Upload new video (Admin only)
- `GET /videos/{id}/questions` - Get video questions

### Questions
- `POST /questions/{id}/answer` - Submit answer to question

### Progress
- `GET /progress/{video_id}` - Get user progress for video
- `PUT /progress/{video_id}` - Update user progress

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables:
   - `VITE_API_URL`: Your backend URL
3. Deploy

### Backend (Render/Railway)
1. Connect your GitHub repository
2. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `GEMEINI_API_KEY`: Your Gemini API key
   - `JWT_SECRET_KEY`: Random secret key
   - `CORS_ORIGINS`: Your frontend URL
3. Deploy

## Development

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### Adding New Features

1. Update database models in `backend/app/models/`
2. Create API endpoints in `backend/app/api/`
3. Update frontend components in `frontend/src/components/`
4. Add new pages in `frontend/src/pages/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
