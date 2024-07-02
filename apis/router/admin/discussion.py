from fastapi import APIRouter
from apis.controller.admin.discussion import create_discussion
from models.admin.discussion import CreateDiscussionParams
from models.common.common import CommonResponse

admin_discussion_router = APIRouter(
    prefix="/admin/discuss",
    tags=["discussion"],
    responses={404: {"description": "Not found"}},
)


@admin_discussion_router.post("/create")
async def create_discussion_api(params: CreateDiscussionParams) -> CommonResponse:
    return create_discussion(params)
