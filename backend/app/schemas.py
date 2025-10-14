from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Video schemas
class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class VideoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    video_url: str
    thumbnail_url: Optional[str]
    duration: Optional[float]
    is_published: bool
    uploader_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class VideoUpload(BaseModel):
    title: str
    description: Optional[str] = None
    question_timestamps: List[float]

# Question schemas
class QuestionResponse(BaseModel):
    id: int
    timestamp: float
    question_type: str
    question_text: str
    options: Optional[List[str]]
    retry_limit: int
    rewind_seconds: float
    is_final_quiz: bool
    
    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    answer: str
    current_timestamp: float

class AnswerResponse(BaseModel):
    correct: bool
    explanation: str
    rewind_seconds: float
    retries_left: int
    summary: Optional[str] = None

# Progress schemas
class ProgressResponse(BaseModel):
    current_timestamp: float
    completed_questions: List[int]
    failed_attempts: Dict[str, int]
    is_completed: bool
    final_score: Optional[float]
    
    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    current_timestamp: float
