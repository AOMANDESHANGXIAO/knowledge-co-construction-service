from models.table_def import Student, NodeTable, NodeTypeDict


def query_group_node_from_student(s, student_id: int) -> int:
    # 查出来讨论的group_id
    student = s.query(Student).filter(Student.id == student_id).first()
    group_id = student.group_id

    group_node = s.query(NodeTable).filter(
        NodeTable.type == NodeTypeDict["group"], NodeTable.group_id == group_id
    ).first()
    group_node_id = group_node.id
    return group_node_id
