from fastapi import APIRouter, HTTPException, status
from models.student.student import StudentSignIn, StudentSignUp
from models.common.common import CommonResponse
from apis.controller.student import student_sign_in, student_sign_up

user_router = APIRouter(
    tags=["Student"]
)


@user_router.post("/signup")
async def sign_up_new_student(params: StudentSignUp) -> CommonResponse:
    """Create a new user"""
    return student_sign_up(params)


@user_router.post("/signin")
async def sign_in_new_student(params: StudentSignIn) -> CommonResponse:
    """User login in"""
    return student_sign_in(params)
