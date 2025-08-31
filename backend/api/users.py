from fastapi import APIRouter,  Depends, HTTPException, status
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from core.security import User, Token,TokenData, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,authenticate_user,get_current_user,get_current_active_user
from sqlalchemy.orm import Session
from core.db import get_db
router = APIRouter(tags=["users"], prefix="/api")


@router.post("/token")
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


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
