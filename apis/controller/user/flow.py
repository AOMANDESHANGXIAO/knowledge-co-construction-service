from datetime import datetime

from models.common.common import CommonResponse, response_success, response_fail
from models.user.flow.flow import FlowGroupNodeData, FlowIdeaNodeData, FlowTopicNodeData, FlowProposeIdeaParams, \
    FlowReplyIdeaParams, FlowReviseGroupConclusionParams, FlowReviseSelfIdeaParams
from models.table_def import NodeTable, EdgeTable, NodeTypeDict, EdgeTypeDict, NodeReviseRecordTable
from db.session import SessionLocal
from crud.node_edge.insert import add_node, add_edge
from crud.student_group.query import query_group_node_from_student
from crud.node_edge.query import query_idea_nodes, query_group_nodes


def query_flow_data(topic_id: int) -> CommonResponse:
    """
    查询出讨论数据，包含edge和node
    :param topic_id:
    :return:
    """
    # 首先查询node_table表
    session = SessionLocal()
    try:
        res_node = []

        idea_nodes = query_idea_nodes(session, topic_id)

        for idea in idea_nodes:
            node = {
                "id": str(idea["node_id"]),
                "type": NodeTypeDict["idea"],
                "data": FlowIdeaNodeData(name=idea["username"], id=idea["node_id"], bgc=idea["group_color"], student_id=idea["student_id"]).__dict__,
                "position": {
                    "x": 0,
                    "y": 0
                }
            }
            res_node.append(node)

        # 一般只会有一个topic_node
        topic_node = session.query(NodeTable).filter(NodeTable.topic_id == topic_id,
                                                     NodeTable.type == NodeTypeDict["topic"]).first()

        res_node.append({
            "id": str(topic_node.id),
            "type": NodeTypeDict["topic"],
            "data": FlowTopicNodeData(text=topic_node.content).__dict__,
            "position": {
                "x": 0,
                "y": 0
            }
        })

        # 查group_node
        group_nodes = query_group_nodes(session, topic_id)

        for group_node in group_nodes:
            res_node.append({
                "id": str(group_node["node_id"]),
                "type": NodeTypeDict["group"],
                "data": FlowGroupNodeData(
                    groupName=group_node["group_name"],
                    groupConclusion=group_node["content"],
                    bgc=group_node["group_color"],
                    group_id=group_node["group_id"]
                ).__dict__,
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


def revise_group_conclusion(params: FlowReviseGroupConclusionParams) -> CommonResponse:
    """
    修改小组 conclusion
    :return:
    """
    session = SessionLocal()

    # 更新节点的node
    session.query(NodeTable).filter(
        NodeTable.group_id == params.group_id,
        NodeTable.topic_id == params.topic_id
    ).update({"content": params.conclusion})

    updated_node = session.query(NodeTable.id).filter(
        NodeTable.group_id == params.group_id,
        NodeTable.topic_id == params.topic_id
    ).first()

    # 修改记录表
    new_revise_record = NodeReviseRecordTable(
        node_id=updated_node.id,
        revise_content=params.conclusion,
        created_time=datetime.now(),
        student_id=params.student_id
    )
    session.add(new_revise_record)
    session.commit()
    return response_success(message="修改成功")


def revise_self_idea(params: FlowReviseSelfIdeaParams) -> CommonResponse:
    """
    修改个人 idea
    :return:
    """
    session = SessionLocal()

    db_node = session.query(NodeTable).filter(NodeTable.id == params.node_id)

    if not db_node:
        return response_fail(message="node_id不存在")
    db_node.update({"content": params.content})
    new_node_revise_record = NodeReviseRecordTable(
        node_id=params.node_id,
        revise_content=params.content,
        created_time=datetime.now(),
        student_id=params.student_id
    )
    session.add(new_node_revise_record)
    session.commit()
    return response_success(message="修改成功")


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


def test_revise_self_idea():
    params = FlowReviseSelfIdeaParams(
        node_id=3,
        content="我的观点是人工智能会改变这个世界，让我们的世界越来来越智能。",
        student_id=4
    )
    print(revise_self_idea(params))

# test_revise_self_idea()
# test_reply_idea()
# test_propose_new_idea()
# test_propose_new_idea()
# test_query_content_data_from_id()
# test_query_flow_data()
