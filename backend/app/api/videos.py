from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.auth import get_current_admin_user
from app.models import User, Video, Question
from app.schemas import VideoResponse, QuestionResponse
from app.services.gemini_service import GeminiService
import os
import whisper
import uuid
import json
import subprocess

WHISPER_MODEL = whisper.load_model("base")

def generate_local_transcript(video_path: str) -> str | None:
    """Uses the local Whisper model to transcribe the video file."""
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None
    
    try:
        print(f"Starting local transcription using Whisper for {video_path}...")
        # Whisper automatically handles many video formats due to FFmpeg being available
        result = WHISPER_MODEL.transcribe(video_path)
        
        # Whisper returns a dictionary containing the transcribed text
        transcript_text = result["text"].strip()
        print("Local transcription completed successfully.")
        return transcript_text
        
    except Exception as e:
        print(f"Error during Whisper transcription: {e}")
        return None

def get_video_duration(video_path: str) -> float:
    """Uses ffprobe (installed in Dockerfile) to extract duration reliably."""
    try:
        # Command to run ffprobe and output duration in seconds
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        print(f"Error calculating video duration: {e}")
        return 0.0

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
        if isinstance(timestamps, (int, float)):
            timestamps = [timestamps]
        if not isinstance(timestamps, list):
            timestamps = []
    except Exception:
        timestamps = []

    # Save video file
    video_filename = f"{uuid.uuid4()}_{video_file.filename}"
    uploads_dir = os.path.join(os.getcwd(), "uploads", "videos")
    os.makedirs(uploads_dir, exist_ok=True)
    video_path = os.path.join(uploads_dir, video_filename)

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

    print(f"Starting transcript generation for file at: {video_path}")
    # Call the local Whisper function you just defined
    transcript = generate_local_transcript(video_path)
    
    if transcript:
        # Store the generated transcript
        video.transcript = transcript

        video.duration = get_video_duration(video_path) 
        print(f"Video duration calculated: {video.duration} seconds")
        
        # Commit the changes (transcript update) to the database
        db.add(video)
        db.commit()
        print("Transcript successfully saved to database.")
    else:
        # If transcription fails, the video.transcript remains None, and the 
        # fallback logic in the next section will handle question generation.
        print("Warning: Transcript generation failed or returned empty. Using fallback questions.")
        
    # Create questions for each timestamp. If transcript is available use OpenAI, otherwise create fallback questions.
    if timestamps:
        for timestamp in timestamps:
            if video.transcript:
                transcript_segment = video.transcript[:int(timestamp * 10)]  # Rough estimate

                # question_data = GeminiService.generate_question(transcript_segment, timestamp, "mcq")
                # question_text = question_data.get("question_text")
                # options = question_data.get("options")
                # correct_answer = question_data.get("correct_answer")
                # explanation = question_data.get("explanation")
                try:
                    question_data = GeminiService.generate_question(transcript_segment, timestamp, "mcq")
                    question_text = question_data.get("question_text")
                    options = question_data.get("options")
                    correct_answer = question_data.get("correct_answer")
                    explanation = question_data.get("explanation")
                except Exception:
                    question_text = f"At {int(timestamp)}s: What is the main idea discussed around this time?"
                    options = ["Main idea A", "Main idea B", "Main idea C", "Main idea D"]
                    correct_answer = "Main idea A"
                    explanation = "Fallback question generated because Gemini failed."
            else:
                # Fallback simple question when no transcript available
                question_text = f"At {int(timestamp)}s: What is the main idea discussed around this time?"
                options = ["Main idea A", "Main idea B", "Main idea C", "Main idea D"]
                correct_answer = "Main idea A"
                explanation = "Fallback question generated because no transcript was available."

            question = Question(
                video_id=video.id,
                timestamp=timestamp,
                question_type="mcq",
                question_text=question_text,
                options=options,
                correct_answer=correct_answer,
                explanation=explanation,
            )
            db.add(question)
        db.commit()

    # Generate a final quiz question at the end of the video
    try:
        final_timestamp = video.duration or 0
        if video.transcript:
            transcript_segment = video.transcript[-1000:] if video.transcript else ""
            final_q = GeminiService.generate_question(transcript_segment, final_timestamp, "mcq")
            fq_text = final_q.get("question_text")
            fq_options = final_q.get("options")
            fq_answer = final_q.get("correct_answer")
            fq_explanation = final_q.get("explanation")
        else:
            fq_text = "Final quiz: What is the main takeaway from this video?"
            fq_options = ["Takeaway A", "Takeaway B", "Takeaway C", "Takeaway D"]
            fq_answer = "Takeaway A"
            fq_explanation = "Fallback final quiz question."

        final_question = Question(
            video_id=video.id,
            timestamp=final_timestamp,
            question_type="mcq",
            question_text=fq_text,
            options=fq_options,
            correct_answer=fq_answer,
            explanation=fq_explanation,
            is_final_quiz=True,
        )
        db.add(final_question)
        db.commit()
    except Exception:
        db.rollback()

    return {"video_id": video.id, "status": "success"}


@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Delete the physical video file
    try:
        video_path = os.path.join(os.getcwd(), video.video_url.lstrip('/'))
        if os.path.exists(video_path):
            os.remove(video_path)
    except Exception as e:
        print(f"Error deleting video file: {e}")

    # Delete associated questions first (due to foreign key constraints)
    db.query(Question).filter(Question.video_id == video_id).delete()
    
    # Delete the video record
    db.delete(video)
    db.commit()

    return {"status": "success", "message": "Video deleted successfully"}

@router.get("/{video_id}/questions", response_model=List[QuestionResponse])
async def get_video_questions(video_id: int, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.video_id == video_id).all()
    return questions
