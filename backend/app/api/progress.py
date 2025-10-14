from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User, UserProgress
from app.schemas import ProgressResponse, ProgressUpdate

router = APIRouter()

@router.get("/{video_id}", response_model=ProgressResponse)
async def get_progress(
    video_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.video_id == video_id
    ).first()
    
    if not progress:
        # Create new progress record
        progress = UserProgress(
            user_id=current_user.id,
            video_id=video_id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

@router.put("/{video_id}")
async def update_progress(
    video_id: int,
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.video_id == video_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            video_id=video_id
        )
        db.add(progress)
    
    progress.current_timestamp = progress_data.current_timestamp
    db.commit()
    
    return {"status": "updated"}
