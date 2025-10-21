from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
from dotenv import load_dotenv
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from core.db import User as DBUser,get_db, UserRole
from pydantic import BaseModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserSubscriptionDTO(BaseModel):
    id: int
    name: str
    quota: int

class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool
    created: datetime | None = None
    updated: datetime | None = None
    role: UserRole | None = None
    subscriptionId: int | None = None
    subscription: UserSubscriptionDTO | None = None

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str,db: Session = Depends(get_db)) -> UserInDB:
    print("username:", repr(username))
    db_user = db.query(DBUser).options(joinedload(DBUser.subscription)).filter(DBUser.username == username).first()
    # print("DB User:", db_user)
    if db_user:
        subscription = (
            UserSubscriptionDTO(
                id=db_user.subscription.id,
                name=db_user.subscription.name,
                quota=db_user.subscription.quota,
            )
            if db_user.subscription
            else None
)

        user = UserInDB(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        disabled=db_user.disabled,
        created=db_user.created,
        updated=db_user.updated,
        hashed_password=db_user.hashed_password,
        role=UserRole(db_user.role) if db_user.role else None,
        subscription= subscription
        )
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


def authenticate_user( username: str, password: str, db: Session = Depends(get_db))-> UserInDB:
    print("username:", repr(username))
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user( token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db))-> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    # Assuming role is an attribute of User model
    if getattr(current_user, "role", None) != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user