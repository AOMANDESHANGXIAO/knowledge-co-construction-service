from fastapi import APIRouter

from apis.controller.flow import query_flow_data
from models.common.common import CommonResponse


flow_router = APIRouter(
    prefix="/flow",
    tags=["flow"],
    responses={404: {"description": "Not found"}},
)


@flow_router.get("/query")
async def query_flow_data_api(topic_id: int) -> CommonResponse:
    return query_flow_data(topic_id)
