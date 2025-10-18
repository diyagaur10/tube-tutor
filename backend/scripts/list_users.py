from app.database import SessionLocal
from app.models.user import User

def list_users():
    db = SessionLocal()
    users = db.query(User).all()
    for u in users:
        print(u.id, u.email, u.username, u.is_admin)

if __name__ == '__main__':
    list_users()
