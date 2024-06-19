from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(
    tags=["Student"]
)

users = {}


@user_router.post("/signup")
async def signup_new_user(data: User) -> dict:
    """Create a new user"""
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email address already exists"
        )
    users[data.email] = data

    return {
        "message": "User successfully registered!"
    }


@user_router.post("/signin")
async def signin_new_user(data: UserSignIn) -> dict:
    """User login in"""
    if data.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    if users[data.email].password != data.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You input a wrong password"
        )

    return {
        "message": "User signed in successfully!"
    }
