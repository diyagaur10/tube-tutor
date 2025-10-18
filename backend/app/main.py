from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api import auth, videos, questions, progress

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="TubeTutor API", version="1.0.0")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Simplified and correct CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(questions.router, prefix="/questions", tags=["questions"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])

@app.get("/")
async def root():
    return {"message": "TubeTutor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
