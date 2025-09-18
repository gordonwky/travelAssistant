from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base 
from core.setting import settings
from sqlalchemy.orm import relationship
from enum import Enum

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    print("Hello you are connecting db")
    try:
        yield db
    finally:
        db.close()

class UserRole(Enum):
    ADMIN = 1
    USER = 2

class UserSubscription( Base):
    __tablename__ = "subscription"
    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    quota = Column(Integer, nullable=False) 
    users = relationship("User", back_populates="subscription")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    disabled = Column(Boolean, default=False)
    role = Column(Integer, default=UserRole.USER, nullable=False)
    approved = Column(Boolean, default=False)
    subscriptionId = Column(Integer, ForeignKey(UserSubscription.id),nullable=True )
    subscription = relationship("UserSubscription", backref="users")
    
