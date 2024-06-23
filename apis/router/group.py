from fastapi import APIRouter
from models.group.group import GroupCreateParams, GroupQueryParams
from models.common.common import CommonResponse
from apis.controller.group import create_group, query_student_group

group_router = APIRouter(
    prefix="/group",
    tags=["group"],
    responses={404: {"description": "Not found"}},
)


@group_router.post("/create")
async def create_group_api(params: GroupCreateParams) -> CommonResponse:
    return create_group(params)


@group_router.get("/query")
async def query_student_group_api(student_id: int) -> CommonResponse:
    return query_student_group(student_id)
