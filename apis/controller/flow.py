from models.common.common import CommonResponse, response_success, response_fail
from models.flow.flow import FlowGroupNodeData, FlowIdeaNodeData, FlowTopicNodeData, FlowProposeIdeaParams
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
    try:
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
                node_id = node.id
                data = FlowIdeaNodeData(name=name, id=node_id).__dict__
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
                "_type": edge.type,
                "animated": True
            })

        return response_success(data={"nodes": res_node, "edges": res_edge})
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def query_content_data_from_id(node_id: int) -> CommonResponse:
    """
    根据node_id查询出node_table表中的内容
    :param node_id:
    :return:
    """
    session = SessionLocal()
    try:
        node = session.query(NodeTable).filter(NodeTable.id == node_id).first()
        if not node:
            return response_fail(message="node_id不存在")

        return response_success(data={"content": node.content})
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def propose_new_idea(params: FlowProposeIdeaParams) -> CommonResponse:
    """
    新增分享观念节点到讨论
    :param params:
    :return:
    """
    session = SessionLocal()
    try:
        # 增添新的节点
        new_node = NodeTable(
            type="idea",
            content=params.content,
            topic_id=params.topic_id,
            student_id=params.student_id,
        )
        session.add(new_node)
        session.flush()
        node_id = new_node.id
        # 增添一个边
        # 查出来讨论的group_id
        student = session.query(Student).filter(Student.id == params.student_id).first()
        group_id = student.group_id

        group_node = session.query(NodeTable).filter(NodeTable.type == "group", NodeTable.group_id == group_id).first()
        group_node_id = group_node.id

        new_edge = EdgeTable(
            type="idea_to_group",
            source=node_id,
            target=group_node_id,
            topic_id=params.topic_id,
        )
        session.add(new_edge)
        session.commit()
        return response_success(message="新增成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


# =================================================
def test_query_flow_data():
    print(query_flow_data(1))


def test_query_content_data_from_id():
    print(query_content_data_from_id(3))


def test_propose_new_idea():
    params = FlowProposeIdeaParams(
        topic_id=1,
        student_id=4,
        content="测试一下"
    )
    print(propose_new_idea(params))

# test_propose_new_idea()
# test_query_content_data_from_id()
# test_query_flow_data()
