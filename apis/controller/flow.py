from models.common.common import CommonResponse, response_success, response_fail
from models.flow.flow import FlowQueryParams, FlowGroupNodeData, FlowIdeaNodeData, FlowTopicNodeData
from models.table_def import NodeTable, EdgeTable, Discussion, Student, Group, Classroom
from db.session import SessionLocal


def query_flow_data(topic_id: int) -> CommonResponse:
    """
    查询出讨论数据，包含edge和node
    :param topic_id:
    :return:
    """
    # 首先查询node_table表
    session = SessionLocal()

    nodes = session.query(NodeTable).filter(NodeTable.topic_id == topic_id)

    res_node = []
    for node in nodes:
        if node.type == "topic":
            data = FlowTopicNodeData(text=node.content).__dict__
            res_node.append({
                "id": str(node.id),
                "type": node.type,
                "data": data,
                "position": {
                    "x": 0,
                    "y": 0
                }
            })
        elif node.type == "idea":
            name = node.from_student.nickname
            s_id = node.from_student.id
            data = FlowIdeaNodeData(name=name, id=s_id).__dict__
            res_node.append({
                "id": str(node.id),
                "type": node.type,
                "data": data,
                "position": {
                    "x": 0,
                    "y": 0
                }
            })
        elif node.type == "group":
            groupName = node.from_group.group_name
            groupConclusion = node.content
            data = FlowGroupNodeData(groupName=groupName, groupConclusion=groupConclusion).__dict__
            res_node.append({
                "id": str(node.id),
                "type": node.type,
                "data": data,
                "position": {
                    "x": 0,
                    "y": 0
                }
            })

    # 查询edge_table表
    edges = session.query(EdgeTable).filter(EdgeTable.topic_id == topic_id)
    res_edge = []
    for edge in edges:
        res_edge.append({
            "id": str(edge.id),
            "source": str(edge.source),
            "target": str(edge.target),
            "type": edge.type,
            "animated": True
        })

    session.close()

    return response_success(data={"nodes": res_node, "edges": res_edge})


def test_query_flow_data():
    print(query_flow_data(FlowQueryParams(topic_id=1)))


# test_query_flow_data()
