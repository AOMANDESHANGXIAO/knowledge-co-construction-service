from fastapi import APIRouter
from models.group.group import GroupCreateParams, GroupJoinParams
from models.common.common import CommonResponse
from apis.controller.group import create_group, query_student_group, join_group, query_group_collaboration_data

group_router = APIRouter(
    prefix="/group",
    tags=["group"],
    responses={404: {"description": "Not found"}},
)


@group_router.post("/create")
async def create_group_api(params: GroupCreateParams) -> CommonResponse:
    return create_group(params)


@group_router.post("/join")
async def join_group_api(params: GroupJoinParams) -> CommonResponse:
    return join_group(params)


@group_router.get("/query")
async def query_student_group_api(student_id: int) -> CommonResponse:
    return query_student_group(student_id)


@group_router.get("/query_collaboration_data")
async def query_group_collaboration_data_api(group_id: int) -> CommonResponse:
    return query_group_collaboration_data(group_id)
