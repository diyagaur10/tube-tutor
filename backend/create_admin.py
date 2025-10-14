#!/usr/bin/env python3
"""
Script to create an admin user for TubeTutor
Run this after setting up the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, Video, Question, UserProgress
from app.auth import get_password_hash
from app.config import settings

def create_admin_user():
    # Create tables
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@tubetutor.com").first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@tubetutor.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("Admin user created successfully!")
        print("Email: admin@tubetutor.com")
        print("Password: admin123")
        print("Username: admin")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
