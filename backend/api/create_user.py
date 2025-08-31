# create_user.py
from core.db import get_db, User
from passlib.context import CryptContext

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(username: str, password: str, email: str = None):
    db = next(get_db())  # get a session
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"User created: {user.username} (id={user.id})")

if __name__ == "__main__":
    create_user("testuser", "testpass", "test@example.com")
