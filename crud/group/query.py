from sqlalchemy import func, case, or_
from models.table_def import NodeTable, EdgeTable, Student, Group, Discussion, NodeReviseRecordTable


def query_group_share_feedback_number(s, group_id: int):
    """
    查询讨论组分享和反馈数量
    :param s:
    :param group_id:
    :return:
    """
    # 构建查询
    query = s.query(
        func.sum(case((EdgeTable.type == 'idea_to_group', 1), else_=0)).label('share'),
        func.sum(case((or_(EdgeTable.type == 'reject', EdgeTable.type == 'approve'), 1), else_=0)).label('feedback')
    ).join(NodeTable, NodeTable.id == EdgeTable.source).join(Student, Student.id == NodeTable.student_id).join(Group,
                                                                                                               Group.id == Student.group_id).filter(
        Group.id == group_id)

    result = query.one()
    return {
        'share': int(result.share) if result.share else 0,
        'feedback': int(result.feedback) if result.feedback else 0
    }


def query_discussion_number(s, class_id: int):
    """
    查询讨论数量
    :param s:
    :param class_id:
    :return:
    """
    # 构建查询
    query = s.query(
        func.count(Discussion.id).label('number')
    ).filter(Discussion.topic_for_class_id == class_id)

    result = query.one()
    return int(result.number if result.number else 0)


def query_summary_number(s, group_id: int):
    """
    查询总结数量
    :param s:
    :param group_id:
    :return:
    """
    # 构建查询
    query = s.query(
        func.count(NodeReviseRecordTable.id).label('number')
    ).join(Student, Student.id == NodeReviseRecordTable.student_id).where(Student.group_id == group_id)

    result = query.one()
    return int(result.number if result.number else 0)


# from db.session import SessionLocal
#
# print(query_summary_number(SessionLocal(), 4))
#

# s = SessionLocal()
# print(query_group_share_feedback_number(s,4))
