from fastapi import APIRouter
from apis.controller.user.discussion import query_all_discussions
from models.common.common import CommonResponse

discussion_router = APIRouter(
    prefix="/discuss",
    tags=["discussion"],
    responses={404: {"description": "Not found"}}
)


@discussion_router.get("/queryTopic")
async def query_all_discussions_api(class_id: int) -> CommonResponse:
    """
    查询班级所有讨论
    """
    return query_all_discussions(class_id)
