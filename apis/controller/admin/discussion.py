from datetime import datetime

from models.common.common import CommonResponse, response_success, response_fail
from db.session import SessionLocal
from models.table_def import Discussion, NodeTable, NodeTypeDict, Group, EdgeTable, EdgeTypeDict
from models.admin.discussion import CreateDiscussionParams


def create_discussion(params: CreateDiscussionParams) -> CommonResponse:
    session = SessionLocal()
    try:
        new_discussion = Discussion(
            topic_content=params.topic_content,
            created_user_id=params.created_user_id,
            topic_for_class_id=params.class_id,
            created_time=datetime.now()
        )
        session.add(new_discussion)
        session.flush()
        # 还要创建节点, 首先是讨论节点
        new_topic_node = NodeTable(
            type=NodeTypeDict["topic"],
            content=params.topic_content,
            class_id=params.class_id,
            group_id=None,
            student_id=None,
            topic_id=new_discussion.id,
            created_time=datetime.now()
        )
        session.add(new_topic_node)
        # 创建小组节点Node
        session.flush()
        # 查出班级所有的小组
        groups = session.query(Group).filter(Group.belong_class_id == params.class_id).all()
        new_group_ids = []
        for group in groups:
            new_group_node = NodeTable(
                type=NodeTypeDict["group"],
                content="",
                class_id=params.class_id,
                group_id=group.id,
                student_id=None,
                topic_id=new_discussion.id,
                created_time=datetime.now()
            )
            session.add(new_group_node)
            session.flush()
            new_group_ids.append(new_group_node.id)
        # 创建边
        for group_id in new_group_ids:
            new_edge = EdgeTable(
                type=EdgeTypeDict["group_to_discuss"],
                source=group_id,
                target=new_topic_node.id,
                topic_id=new_discussion.id
            )
            session.add(new_edge)
        session.commit()
        return response_success(message="创建成功")
    except Exception as e:
        session.rollback()
        return response_fail(message=str(e))
    finally:
        session.close()
