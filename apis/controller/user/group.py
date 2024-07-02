from sqlalchemy import desc, and_

from models.user.group.group import GroupCreateParams, GroupJoinParams, GroupInfo
from models.common.common import CommonResponse, response_success, response_fail
from db.session import SessionLocal
from models.table_def import Group, Student, NodeReviseRecordTable, NodeTable
from crud.group.query import query_group_share_feedback_number, query_discussion_number, query_summary_number, \
    query_group_student_propose_feedback_data, query_group_student_summary_data


def create_group(params: GroupCreateParams) -> CommonResponse:
    session = SessionLocal()
    try:
        # 查询创建团队的学生是否已经有团队了，有的话就拒绝创建
        db_student = session.query(Student).filter(Student.id == params.student_id).first()
        if db_student.group_id:
            # print("the group_id =", db_student.group_id)
            return response_fail(message="该学生已经有团队了")

        # 组名不能重复
        db_group = session.query(Group).filter(Group.group_name == params.group_name).first()

        if db_group:
            return response_fail(message="组名重复")

        # 否则插入一个组到数据库
        new_group = Group(
            **{
                "group_name": params.group_name,
                "group_description": params.group_description,
                "belong_class_id": params.class_id,
                "group_color": params.group_color
            }
        )
        # 要拿到新插入数据的主键
        session.add(new_group)
        session.flush()
        session.refresh(new_group)  # 刷新数据才能拿到主键

        # 为团队生成团队码，格式为: ckc+id
        session.query(Group).filter(Group.id == new_group.id).update({"group_code": f"ckc{new_group.id}"})

        # 更新创建团队的学生的group_id
        session.query(Student).filter(Student.id == params.student_id).update({"group_id": new_group.id})

        session.commit()

        data = GroupInfo(**{
            "group_id": new_group.id,
            "group_name": new_group.group_name,
            "group_description": new_group.group_description,
            "group_code": new_group.group_code,
            "group_color": new_group.group_color,
            "belong_class_id": new_group.belong_class_id,
        })

        return response_success(message="创建成功", data=data.__dict__)
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def join_group(params: GroupJoinParams) -> CommonResponse:
    session = SessionLocal()
    try:
        db_group = session.query(Group).filter(Group.group_code == params.group_code).first()

        if not db_group:
            return response_fail(message="团队不存在")

        db_student = session.query(Student).filter(Student.id == params.student_id).first()

        if db_student.group_id:
            return response_fail(message="该学生已在团队中")

        session.query(Student).filter(Student.id == params.student_id).update({"group_id": db_group.id})

        session.commit()

        return response_success(data={
            "group_id": db_group.id,
            "group_name": db_group.group_name,
            "group_description": db_group.group_description,
            "group_code": db_group.group_code,
            "group_color": db_group.group_color,
            "belong_class_id": db_group.belong_class_id,
        }, message="加入成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def query_student_group(student_id: int) -> CommonResponse:
    session = SessionLocal()
    try:
        db_student = session.query(Student).filter(Student.id == student_id).first()
        if not db_student.group_id:
            return response_fail(message="该学生没有团队")

        db_group = db_student.group

        return response_success(data={
            "group_id": db_group.id,
            "group_name": db_group.group_name,
            "group_description": db_group.group_description,
            "group_code": db_group.group_code,
            "group_color": db_group.group_color,
            "belong_class_id": db_group.belong_class_id,
        })
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def query_group_collaboration_data(group_id: int) -> CommonResponse:
    session = SessionLocal()
    try:
        share_feedback_data = query_group_share_feedback_number(s=session, group_id=group_id)

        db_group = session.query(Group).filter(Group.id == group_id).first()

        discussion_data = query_discussion_number(s=session, class_id=db_group.belong_class_id)

        summary_data = query_summary_number(s=session, group_id=group_id)

        # 依据前端格式要求返回
        data = {
            "list": [
                {
                    "iconName": "discussion",
                    "text": "参与了讨论",
                    "num": discussion_data
                },
                {
                    "iconName": "share",
                    "text": "分享过观点",
                    "num": share_feedback_data["share"]
                },
                {
                    "iconName": "feedback",
                    "text": "反馈过观点",
                    "num": share_feedback_data["feedback"]
                },
                {
                    "iconName": "summary",
                    "text": "总结过观点",
                    "num": summary_data
                }
            ]
        }
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()
    return response_success(data=data)


def query_group_member_data(group_id: int) -> CommonResponse:
    session = SessionLocal()
    feedback_propose_list = query_group_student_propose_feedback_data(session, group_id)

    feedback_list_data = []
    propose_list_data = []

    for item in feedback_propose_list:
        feedback_list_data.append({
            "value": item["feedbackNum"],
            "name": item["name"]
        })
        propose_list_data.append(({
            "value": item["proposeNum"],
            "name": item["name"]
        }))

    summary_list = query_group_student_summary_data(session, group_id)

    summary_list_data = [
        {
            "value": item["summaryNum"],
            "name": item["name"]
        } for item in summary_list
    ]

    return response_success(data={
        "feedbackList": feedback_list_data,
        "proposeList": propose_list_data,
        "summaryList": summary_list_data
    })


def query_group_revise_data(group_id: int, topic_id: int) -> CommonResponse:
    session = SessionLocal()
    # 查NodeReviseRecordTable表
    try:
        query = (session.query(
            NodeReviseRecordTable.revise_content,
            Student.nickname,
            NodeReviseRecordTable.created_time
        ).join(
            Student,
            NodeReviseRecordTable.student_id == Student.id
        ).join(
            Group,
            Group.id == Student.group_id
        ).join(
            NodeTable,
            and_(
                NodeTable.topic_id == topic_id,
                NodeReviseRecordTable.node_id == NodeTable.id
            )
        ).filter(Group.id == group_id).order_by(desc(NodeReviseRecordTable.created_time)).limit(5))

        results = query.all()

        data = {
            "list": [
                {
                    "content": r.revise_content,
                    "creator": r.nickname,
                    "timestamp": r.created_time
                }
                for r in results
            ]
        }
        return response_success(data=data)
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


# ======================================================
def test_create_group() -> CommonResponse:
    params = GroupCreateParams(
        group_name="test_group4",
        group_description="test_group_description",
        class_id=1,
    )
    return create_group(params)


def test_query_student_group() -> CommonResponse:
    return query_student_group(student_id=1)


def test_simple_join_group(params: GroupJoinParams):
    session = SessionLocal()
    db_group = session.query(Group).filter(Group.group_code == params.group_code).first()

    if not db_group:
        return response_fail(message="团队不存在")

    db_student = session.query(Student).filter(Student.id == params.student_id).first()

    if db_student.group_id:
        return response_fail(message="该学生已在团队中")

    session.query(Student).filter(Student.id == params.student_id).update({"group_id": db_group.id})

    session.commit()

    return response_success(data={
        "group_id": db_group.id,
        "group_name": db_group.group_name,
        "group_description": db_group.group_description,
        "group_code": db_group.group_code,
        "group_color": db_group.group_color,
        "belong_class_id": db_group.belong_class_id,
    }, message="加入成功")


def test_join_group() -> CommonResponse:
    params = GroupJoinParams(
        student_id=1,
        group_code="ckc10"
    )
    return test_simple_join_group(params)


def test_query_group_collaboration_data():
    print(query_group_collaboration_data(group_id=4))


def test_query_group_member_data():
    print(query_group_member_data(group_id=4))


def test_query_group_revise_data():
    print(query_group_revise_data(group_id=4, topic_id=1))
# test_query_group_revise_data()
# test_query_group_member_data()
# test_query_group_collaboration_data()
# print(test_join_group())
# print(test_query_student_group())
# print(test_create_group())
