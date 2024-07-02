from fastapi import APIRouter
from apis.controller.admin.sign import admin_sign_in, admin_sign_up
from models.admin.adminer import AdminerSignInParams, AdminerSignUpParams
from models.common.common import CommonResponse

admin_sign_router = APIRouter(
    prefix="/admin/sign",
    tags=["admin_sign"],
    responses={404: {"description": "Not found"}},
)


@admin_sign_router.post("/signin")
async def admin_sign_in_api(params: AdminerSignInParams) -> CommonResponse:
    return admin_sign_in(params)


@admin_sign_router.post("/signup")
async def admin_sign_up_api(params: AdminerSignUpParams) -> CommonResponse:
    return admin_sign_up(params)
