from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User, Question, UserProgress
from app.schemas import AnswerSubmit, AnswerResponse
from app.services.gemini_service import GeminiService

router = APIRouter()

@router.post("/{question_id}/answer", response_model=AnswerResponse)
async def submit_answer(
    question_id: int,
    answer_data: AnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get question
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Get or create user progress
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.video_id == question.video_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            video_id=question.video_id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    # Check if already completed
    if question_id in (progress.completed_questions or []):
        return AnswerResponse(
            correct=True,
            explanation="Already completed",
            rewind_seconds=0,
            retries_left=0
        )
    
    # Grade the answer
    grading_result = GeminiService.grade_answer(
        question.question_text,
        answer_data.answer,
        question.correct_answer
    )
    
    # Update failed attempts
    failed_attempts = progress.failed_attempts or {}
    attempts = failed_attempts.get(str(question_id), 0)
    
    if grading_result["correct"]:
        # Mark as completed
        completed_questions = progress.completed_questions or []
        completed_questions.append(question_id)
        progress.completed_questions = completed_questions
        
        # Update current timestamp
        progress.current_timestamp = answer_data.current_timestamp
        
        db.commit()
        
        return AnswerResponse(
            correct=True,
            explanation=grading_result["explanation"],
            rewind_seconds=0,
            retries_left=question.retry_limit - attempts
        )
    else:
        # Increment failed attempts
        attempts += 1
        failed_attempts[str(question_id)] = attempts
        progress.failed_attempts = failed_attempts
        
        db.commit()
        
        retries_left = max(0, question.retry_limit - attempts)
        
        if retries_left == 0:
            # Generate summary for failed question
            summary = GeminiService.generate_summary(
                question.video.transcript or "",
                question.question_text
            )
            
            return AnswerResponse(
                correct=False,
                explanation=grading_result["explanation"],
                rewind_seconds=question.rewind_seconds,
                retries_left=0,
                summary=summary
            )
        else:
            return AnswerResponse(
                correct=False,
                explanation=grading_result["explanation"],
                rewind_seconds=0,
                retries_left=retries_left
            )
