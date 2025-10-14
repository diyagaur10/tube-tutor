# Import all models here to ensure they are registered with SQLAlchemy
from app.models.user import User
from app.models.video import Video
from app.models.question import Question
from app.models.progress import UserProgress

__all__ = ["User", "Video", "Question", "UserProgress"]
