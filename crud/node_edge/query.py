from models.table_def import NodeTable, Student, Group


def query_idea_nodes(s, topic_id: int):
    """
    查询类型为'idea'的节点及其关联的学生用户名
    :param topic_id: 讨论主题ID
    :return: 查询结果
    """
    # 使用left join和filter_by来构建查询
    query = (
        s.query(
            NodeTable.id.label('node_id'),
            NodeTable.content,
            Student.nickname,
            Group.group_color,
            Student.id
        )
        .outerjoin(Student, NodeTable.student_id == Student.id)
        .join(Group, Group.id == Student.group_id)
        .filter(NodeTable.type == 'idea', NodeTable.topic_id == topic_id)
    )

    # 执行查询并获取所有结果
    results = query.all()

    # 根据需要处理结果，例如转换为字典列表
    nodes_data = [
        {
            "node_id": result.node_id,
            "content": result.content,
            "username": result.nickname,
            "group_color": result.group_color,
            "student_id": result.id
        }
        for result in results
    ]

    return nodes_data


def query_group_nodes(s, topic_id: int):
    """
    查询类型为'group'的节点及其关联的学生用户名
    :param topic_id: 讨论主题ID
    :return: 查询结果
    """
    # 使用left join和filter_by来构建查询
    query = (
        s.query(
            NodeTable.id.label('node_id'),
            NodeTable.content,
            Group.group_name,
            Group.group_color,
            Group.id
        )
        .join(Group, Group.id == NodeTable.group_id)
        .where(NodeTable.type == "group", NodeTable.topic_id == topic_id)
    )
    results = query.all()
    nodes_data = [
        {
            "node_id": result.node_id,
            "content": result.content,
            "group_name": result.group_name,
            "group_color": result.group_color,
            "group_id": result.id
        }
        for result in results
    ]
    return nodes_data

#
# from db.session import SessionLocal
#
# session = SessionLocal()
# print(query_group_nodes(session, 1))
# print(query_idea_nodes(1))
