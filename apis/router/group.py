from fastapi import APIRouter
from models.group.group import GroupCreateParams
from models.common.common import CommonResponse
from apis.controller.group import create_group

group_router = APIRouter(
    prefix="/group",
    tags=["group"],
    responses={404: {"description": "Not found"}},
)


@group_router.post("/create")
def create_group_api(params: GroupCreateParams) -> CommonResponse:
    return create_group(params)
