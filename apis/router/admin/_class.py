from fastapi import APIRouter
from apis.controller.admin.classManage import CreateClassParams, create_class, drop_class, query_class_list
from models.admin.classManage import DropClassParams
from models.common.common import CommonResponse

_class_router = APIRouter(
    prefix="/admin/class",
    tags=["class"],
    responses={404: {"description": "Not found"}},
)


@_class_router.post("/create")
async def create_class_api(params: CreateClassParams) -> CommonResponse:
    return create_class(params)


@_class_router.post("/drop")
async def drop_class_api(params: DropClassParams) -> CommonResponse:
    return drop_class(params)


@_class_router.get("/list")
async def query_class_list_api() -> CommonResponse:
    return query_class_list()
