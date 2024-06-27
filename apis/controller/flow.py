from models.common.common import CommonResponse, response_success, response_fail
from models.flow.flow import FlowGroupNodeData, FlowIdeaNodeData, FlowTopicNodeData, FlowProposeIdeaParams, \
    FlowReplyIdeaParams
from models.table_def import NodeTable, EdgeTable, Discussion, Student, Group, Classroom, NodeTypeDict, EdgeTypeDict
from db.session import SessionLocal
from crud.node_edge.insert import add_node, add_edge
from crud.student_group.query import query_group_node_from_student


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
            if node.type == NodeTypeDict["topic"]:
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
            elif node.type == NodeTypeDict["idea"]:
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
            elif node.type == NodeTypeDict["group"]:
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
        new_node_id = add_node(
            session,
            _type=NodeTypeDict["idea"],
            topic_id=params.topic_id,
            student_id=params.student_id,
            content=params.content
        )

        group_node_id = query_group_node_from_student(session, params.student_id)

        add_edge(
            session,
            _type=EdgeTypeDict["idea_to_group"],
            source=new_node_id,
            target=group_node_id,
            topic_id=params.topic_id,
        )

        session.commit()
        return response_success(message="新增成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def reply_idea(params: FlowReplyIdeaParams) -> CommonResponse:
    """
    新增分享观念节点到讨论
    :param params:
    :return:
    """
    session = SessionLocal()
    try:

        # 添加新节点
        new_node_id = add_node(
            session,
            _type=NodeTypeDict["idea"],
            topic_id=params.topic_id,
            student_id=params.student_id,
            content=params.content
        )

        # 添加新的边
        new_edge_type = EdgeTypeDict["approve"] if params.reply_type else EdgeTypeDict["reject"]

        add_edge(
            session,
            _type=new_edge_type,
            source=new_node_id,
            target=params.reply_to,
            topic_id=params.topic_id,
        )

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
    """
        新增分享观念节点到讨论
        :param params:
        :return:
    """
    session = SessionLocal()

    new_node_id = add_node(
        session,
        _type=NodeTypeDict["idea"],
        topic_id=params.topic_id,
        student_id=params.student_id,
        content=params.content
    )

    group_node_id = query_group_node_from_student(session, params.student_id)

    add_edge(
        session,
        _type=EdgeTypeDict["idea_to_group"],
        source=new_node_id,
        target=group_node_id,
        topic_id=params.topic_id,
    )

    session.commit()
    print(response_success(message="新增成功"))
    return response_success(message="新增成功")


def test_reply_idea():
    params = FlowReplyIdeaParams(
        topic_id=1,
        student_id=4,
        content="我有意见",
        reply_to=3,
        reply_type=0
    )
    print(reply_idea(params))

# test_reply_idea()
# test_propose_new_idea()
# test_propose_new_idea()
# test_query_content_data_from_id()
# test_query_flow_data()
