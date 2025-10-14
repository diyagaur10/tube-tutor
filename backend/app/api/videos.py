from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.auth import get_current_user, get_current_admin_user
from app.models import User, Video, Question, UserProgress
from app.schemas import VideoCreate, VideoResponse, VideoUpload, QuestionResponse
from app.services.openai_service import OpenAIService
import os
import uuid
import json

router = APIRouter()

@router.get("/", response_model=List[VideoResponse])
async def get_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.is_published == True).all()
    return videos

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.post("/upload", response_model=dict)
async def upload_video(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    question_timestamps: str = Form(...),  # JSON string
    video_file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Parse question timestamps
    try:
        timestamps = json.loads(question_timestamps)
    except:
        timestamps = []
    
    # Save video file
    video_filename = f"{uuid.uuid4()}_{video_file.filename}"
    video_path = f"uploads/videos/{video_filename}"
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    
    with open(video_path, "wb") as buffer:
        content = await video_file.read()
        buffer.write(content)
    
    # Create video record
    video = Video(
        title=title,
        description=description,
        video_url=f"/uploads/videos/{video_filename}",
        uploader_id=current_user.id,
        is_published=True
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    
    # Generate questions for each timestamp
    if video.transcript and timestamps:
        for timestamp in timestamps:
            # Get transcript segment up to timestamp
            transcript_segment = video.transcript[:int(timestamp * 10)]  # Rough estimate
            
            # Generate question
            question_data = OpenAIService.generate_question(
                transcript_segment, timestamp, "mcq"
            )
            
            question = Question(
                video_id=video.id,
                timestamp=timestamp,
                question_type="mcq",
                question_text=question_data["question_text"],
                options=question_data.get("options"),
                correct_answer=question_data["correct_answer"],
                explanation=question_data["explanation"]
            )
            db.add(question)
    
    db.commit()
    
    return {"video_id": video.id, "status": "success"}

@router.get("/{video_id}/questions", response_model=List[QuestionResponse])
async def get_video_questions(video_id: int, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.video_id == video_id).all()
    return questions
