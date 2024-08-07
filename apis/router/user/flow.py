from fastapi import APIRouter

from apis.controller.user.flow import query_flow_data, query_content_data_from_id, propose_new_idea, reply_idea, \
    revise_group_conclusion, revise_self_idea
from models.common.common import CommonResponse
from models.user.flow.flow import FlowProposeIdeaParams, FlowReplyIdeaParams, FlowReviseGroupConclusionParams, \
    FlowReviseSelfIdeaParams

flow_router = APIRouter(
    prefix="/flow",
    tags=["flow"],
    responses={404: {"description": "Not found"}},
)


@flow_router.get("/query")
async def query_flow_data_api(topic_id: int) -> CommonResponse:
    """
    查询话题包含的节点信息以及边信息
    :param topic_id:
    :return:
    """
    return query_flow_data(topic_id)


@flow_router.get("/query_content")
async def query_content_data_from_id_api(node_id: int) -> CommonResponse:
    """
    根据节点id查询包含的内容
    :param node_id:
    :return:
    """
    return query_content_data_from_id(node_id)


@flow_router.post("/propose_idea")
async def propose_new_idea_api(params: FlowProposeIdeaParams) -> CommonResponse:
    """
    学生提交新的想法
    :param params:
    :return:
    """
    return propose_new_idea(params)


@flow_router.post('/reply_idea')
async def reply_idea_api(params: FlowReplyIdeaParams) -> CommonResponse:
    """
    回复观点
    :param params:
    :return:
    """
    return reply_idea(params)


@flow_router.post('/revise_group_conclusion')
async def revise_group_conclusion_api(params: FlowReviseGroupConclusionParams) -> CommonResponse:
    """
    修改团队结论
    :param params:
    :return:
    """
    return revise_group_conclusion(params)


@flow_router.post('/revise_self_idea')
async def revise_self_idea_api(params: FlowReviseSelfIdeaParams) -> CommonResponse:
    """
    修改自己的想法
    """
    return revise_self_idea(params)
