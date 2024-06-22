from fastapi import APIRouter
from apis.controller.classroom import query_classroom_list
from models.common.common import CommonResponse

classroom_router = APIRouter(
    prefix="/classroom",
    tags=["classroom"],
    responses={404: {"description": "Not found"}},
)


@classroom_router.get("/queryClassroomList")
def query_classroom_list_api() -> CommonResponse:
    return query_classroom_list()
