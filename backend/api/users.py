from fastapi import APIRouter,  Depends, HTTPException, status
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from core.security import User, Token, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,authenticate_user,get_current_active_user, get_password_hash, get_current_active_admin
from sqlalchemy.orm import Session
from core.db import get_db, User as DBUser, UserRole, UserSubscription

router = APIRouter(tags=["users"], prefix="/api")


@router.post("/signup", response_model = dict)
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> dict:
    user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    new_user = DBUser(
        username=form_data.username,
        email=form_data.username,  # Assuming email is the same as username
        hashed_password=get_password_hash(form_data.password),  # In a real app, hash the password
        role=UserRole.USER,  # Default role
        subscription=UserSubscription.FREE  # Default subscription

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully and waiting for approval."}

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    print("username:", form_data.username)
    print("password:", form_data.password)
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/logout")
async def logout(current_user: Annotated[User, Depends(get_current_active_user)]):
    # Invalidate the user's token or perform any logout logic here
    return {"message": "Successfully logged out"}

@router.get("/users/", response_model=list[User])
async def read_users(current_user: Annotated[User, Depends(get_current_active_admin)],skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    current_user
    users = db.query(DBUser).offset(skip).limit(limit).all()
    return users

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
