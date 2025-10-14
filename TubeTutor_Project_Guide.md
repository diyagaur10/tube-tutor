# TubeTutor - YouTube-like Learning Platform

## 1. Project Scaffold

```
teach-tube/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── video.py
│   │   │   ├── question.py
│   │   │   └── progress.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── videos.py
│   │   │   ├── questions.py
│   │   │   └── progress.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── openai_service.py
│   │   │   ├── transcription_service.py
│   │   │   └── video_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoPlayer/
│   │   │   │   ├── VideoPlayer.jsx
│   │   │   │   ├── QuestionModal.jsx
│   │   │   │   └── ProgressBar.jsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   └── RegisterForm.jsx
│   │   │   ├── admin/
│   │   │   │   ├── VideoUpload.jsx
│   │   │   │   └── QuestionConfig.jsx
│   │   │   └── common/
│   │   │       ├── Header.jsx
│   │   │       └── Layout.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── VideoPage.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   └── Profile.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useVideo.js
│   │   │   └── useQuestions.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── auth.js
│   │   ├── utils/
│   │   │   ├── constants.js
│   │   │   └── helpers.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
├── docker-compose.yml
├── README.md
└── .gitignore
```

## 2. DB Schema and SQLAlchemy Models

### User Model
```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    videos = relationship("Video", back_populates="uploader")
    progress = relationship("UserProgress", back_populates="user")
```

### Video Model
```python
# backend/app/models/video.py
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    video_url = Column(String, nullable=False)
    thumbnail_url = Column(String)
    duration = Column(Float)  # in seconds
    transcript = Column(Text)
    is_published = Column(Boolean, default=False)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    uploader = relationship("User", back_populates="videos")
    questions = relationship("Question", back_populates="video")
    progress = relationship("UserProgress", back_populates="video")
```

### Question Model
```python
# backend/app/models/question.py
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    timestamp = Column(Float, nullable=False)  # seconds into video
    question_type = Column(String, nullable=False)  # "mcq", "fill_in", "one_word"
    question_text = Column(Text, nullable=False)
    options = Column(JSON)  # for MCQ: ["option1", "option2", ...]
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text)
    retry_limit = Column(Integer, default=3)
    rewind_seconds = Column(Float, default=30.0)
    is_final_quiz = Column(Boolean, default=False)
    
    video = relationship("Video", back_populates="questions")
```

### User Progress Model
```python
# backend/app/models/progress.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))
    current_timestamp = Column(Float, default=0.0)
    completed_questions = Column(JSON, default=list)  # [question_id, ...]
    failed_attempts = Column(JSON, default=dict)  # {question_id: count}
    is_completed = Column(Boolean, default=False)
    final_score = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="progress")
    video = relationship("Video", back_populates="progress")
```

## 3. FastAPI Endpoints

### Auth Endpoints
```python
# POST /auth/register
{
  "username": "string",
  "email": "string", 
  "password": "string"
}
# Response: {"access_token": "string", "user": {...}}

# POST /auth/login
{
  "email": "string",
  "password": "string"
}
# Response: {"access_token": "string", "user": {...}}
```

### Video Endpoints
```python
# GET /videos/
# Response: [{"id": 1, "title": "string", "thumbnail_url": "string", ...}]

# GET /videos/{video_id}
# Response: {"id": 1, "title": "string", "video_url": "string", "transcript": "string", ...}

# POST /videos/upload (Admin only)
{
  "title": "string",
  "description": "string",
  "video_file": "file",
  "question_timestamps": [30.0, 120.0, 300.0]
}
# Response: {"video_id": 1, "status": "processing"}
```

### Question Endpoints
```python
# GET /videos/{video_id}/questions
# Response: [{"id": 1, "timestamp": 30.0, "question_text": "string", ...}]

# POST /questions/{question_id}/answer
{
  "answer": "string",
  "current_timestamp": 35.0
}
# Response: {
#   "correct": true,
#   "explanation": "string",
#   "rewind_seconds": 0,
#   "retries_left": 2
# }
```

### Progress Endpoints
```python
# GET /progress/{video_id}
# Response: {"current_timestamp": 35.0, "completed_questions": [1, 2], ...}

# PUT /progress/{video_id}
{
  "current_timestamp": 40.0
}
# Response: {"status": "updated"}
```

## 4. React VideoPlayer Component Outline

```jsx
// frontend/src/components/VideoPlayer/VideoPlayer.jsx
import { useState, useEffect, useRef } from 'react';
import QuestionModal from './QuestionModal';

const VideoPlayer = ({ videoId, videoUrl }) => {
  const videoRef = useRef(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [questions, setQuestions] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [isBlocked, setIsBlocked] = useState(false);
  const [progress, setProgress] = useState({});

  // Load questions and progress on mount
  useEffect(() => {
    loadQuestions();
    loadProgress();
  }, [videoId]);

  // Check for questions at current timestamp
  useEffect(() => {
    const question = questions.find(q => 
      Math.abs(q.timestamp - currentTime) < 2 && 
      !progress.completed_questions?.includes(q.id)
    );
    
    if (question && !isBlocked) {
      triggerQuestion(question);
    }
  }, [currentTime, questions, progress]);

  const triggerQuestion = (question) => {
    setIsBlocked(true);
    setCurrentQuestion(question);
    setShowModal(true);
    videoRef.current?.pause();
  };

  const handleAnswerSubmit = async (answer) => {
    const response = await submitAnswer(currentQuestion.id, answer, currentTime);
    
    if (response.correct) {
      setShowModal(false);
      setIsBlocked(false);
      updateProgress(currentQuestion.id);
      videoRef.current?.play();
    } else {
      if (response.retries_left > 0) {
        // Show explanation and allow retry
        showExplanation(response.explanation);
      } else {
        // Rewind video
        const newTime = Math.max(0, currentTime - response.rewind_seconds);
        videoRef.current.currentTime = newTime;
        setShowModal(false);
        setIsBlocked(false);
      }
    }
  };

  const handleSeek = (newTime) => {
    if (isBlocked) {
      // Prevent seeking when question is active
      return false;
    }
    
    // Check if seeking past incomplete questions
    const incompleteQuestion = questions.find(q => 
      q.timestamp <= newTime && 
      !progress.completed_questions?.includes(q.id)
    );
    
    if (incompleteQuestion) {
      // Block seeking past incomplete questions
      return false;
    }
    
    return true;
  };

  return (
    <div className="video-container">
      <video
        ref={videoRef}
        src={videoUrl}
        onTimeUpdate={(e) => setCurrentTime(e.target.currentTime)}
        onSeeked={(e) => {
          if (!handleSeek(e.target.currentTime)) {
            e.target.currentTime = currentTime;
          }
        }}
        controls={!isBlocked}
        className="w-full"
      />
      
      <QuestionModal
        isOpen={showModal}
        question={currentQuestion}
        onSubmit={handleAnswerSubmit}
        onClose={() => {
          setShowModal(false);
          setIsBlocked(false);
        }}
      />
    </div>
  );
};
```

## 5. OpenAI Prompts

### Question Generation Prompt
```python
def generate_question_prompt(transcript_segment, timestamp, question_type):
    return f"""
    Based on the video transcript up to timestamp {timestamp} seconds, generate a {question_type} question.
    
    Transcript: {transcript_segment}
    
    Requirements:
    - Question should test understanding of key concepts mentioned
    - For MCQ: Provide 4 options with only one correct answer
    - For fill-in: Create a sentence with a blank to fill
    - For one-word: Ask for a specific term or concept
    - Make it challenging but fair based on the content shown
    
    Return JSON format:
    {{
        "question_text": "string",
        "options": ["option1", "option2", "option3", "option4"], // only for MCQ
        "correct_answer": "string",
        "explanation": "string"
    }}
    """
```

### Answer Grading Prompt
```python
def grade_answer_prompt(question, user_answer, correct_answer):
    return f"""
    Grade this answer for a learning video question.
    
    Question: {question}
    Correct Answer: {correct_answer}
    User Answer: {user_answer}
    
    Return JSON:
    {{
        "correct": boolean,
        "explanation": "Brief explanation of why the answer is correct/incorrect",
        "hint": "Optional hint for incorrect answers"
    }}
    
    Be lenient with minor variations in spelling/formatting for correct answers.
    """
```

### Summary Prompt
```python
def generate_summary_prompt(transcript_segment, failed_question):
    return f"""
    The student failed to answer this question correctly: {failed_question}
    
    Based on the video content up to this point, provide a brief summary (2-3 sentences) 
    that helps the student understand the key concepts they need to know.
    
    Transcript segment: {transcript_segment}
    
    Focus on the most important points that would help answer the question correctly.
    Keep it concise and encouraging.
    """
```

## 6. Deployment Notes

### Frontend (Vercel)
```bash
# Build command
npm run build

# Environment variables
VITE_API_URL=https://your-backend-url.com
VITE_APP_NAME=TubeTutor
```

### Backend (Render/Railway)
```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Environment variables
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your-secret
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### Database Setup
```bash
# Run migrations
alembic upgrade head

# Create admin user
python scripts/create_admin.py
```

### Docker Compose (Development)
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: tubetutor
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/tubetutor
    depends_on:
      - db
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:8000
```
