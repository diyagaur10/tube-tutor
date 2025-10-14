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
