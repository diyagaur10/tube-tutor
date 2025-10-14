from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

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
