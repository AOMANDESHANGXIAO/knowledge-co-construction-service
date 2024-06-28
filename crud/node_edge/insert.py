from datetime import datetime

from models.table_def import NodeTable, EdgeTable


def add_node(s, _type, content, topic_id, student_id):
    new_node = NodeTable(
        type=_type,
        content=content,
        topic_id=topic_id,
        student_id=student_id,
        created_time=datetime.now()
    )
    s.add(new_node)
    s.flush()
    return new_node.id


def add_edge(s, _type, source, target, topic_id):
    new_edge = EdgeTable(
        type=_type,
        source=source,
        target=target,
        topic_id=topic_id
    )
    s.add(new_edge)

