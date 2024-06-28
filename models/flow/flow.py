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
    bgc: str  # 发言学生颜色和组的颜色一致


class FlowGroupNodeData(BaseModel):
    """
    前端要求的类型为group的节点的数据格式
    """
    groupName: str  # 讨论组名称
    groupConclusion: str  # 讨论组得出的结论
    bgc: str  # 讨论组颜色


class FlowProposeIdeaParams(BaseModel):
    """
    分享观点的请求参数
    """
    topic_id: int
    student_id: int
    content: str


class FlowReplyIdeaParams(BaseModel):
    """
    回复观点的请求参数
    """
    topic_id: int
    student_id: int
    content: str
    reply_to: int  # 回复的节点id
    reply_type: int  # 0 表示反驳 1表示赞成


class FlowReviseGroupConclusionParams(BaseModel):
    """
    修改讨论组的结论的请求参数
    """
    topic_id: int
    student_id: int
    group_id: int
    conclusion: str
