from pydantic import BaseModel


class FlowQueryParams(BaseModel):
    """
    进入讨论话题请求参数
    """
    topic_id: int


class FlowTopicNodeData(BaseModel):
    """
    前端要求的类型为topic的节点的数据格式
    """
    text: str


class FlowIdeaNodeData(BaseModel):
    """
    前端要求的类型为idea的节点的数据格式
    """
    name: str  # 发言学生姓名
    id: int  # 发言学生id


class FlowGroupNodeData(BaseModel):
    """
    前端要求的类型为group的节点的数据格式
    """
    groupName: str  # 讨论组名称
    groupConclusion: str  # 讨论组得出的结论


class FlowProposeIdeaParams(BaseModel):
    """
    分享观点的请求参数
    """
    topic_id: int
    student_id: int
    content: str
