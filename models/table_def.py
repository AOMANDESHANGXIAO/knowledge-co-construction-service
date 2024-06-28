from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.annotated_type import int_pk, required_unique_name, required_string, timestamp_default_now, string_255, \
    string_128, string_1000

Base = declarative_base()


class Classroom(Base):
    __tablename__ = 'class'
    __table_args__ = {'comment': '班级信息表'}

    id: Mapped[int_pk]
    class_name: Mapped[required_unique_name]

    students: Mapped[list["Student"]] = relationship(back_populates="classroom")
    discussions: Mapped[list["Discussion"]] = relationship(back_populates="related_class")
    groups: Mapped[list["Group"]] = relationship(lazy=True, back_populates="belong_classroom")
    nodes: Mapped[list["NodeTable"]] = relationship(back_populates="from_classroom")


class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'comment': '协作团队信息表'}

    id: Mapped[int_pk]
    group_name: Mapped[required_unique_name]
    group_description: Mapped[required_string]
    group_code: Mapped[required_unique_name]
    group_color: Mapped[string_255]
    belong_class_id: Mapped[int] = mapped_column(ForeignKey("class.id"), nullable=True)

    belong_classroom: Mapped["Classroom"] = relationship(lazy=True, back_populates="groups")
    students: Mapped[list["Student"]] = relationship(lazy=True, back_populates="group")
    nodes: Mapped[list["NodeTable"]] = relationship(back_populates="from_group")


class Student(Base):
    __tablename__ = 'student'
    __table_args__ = {'comment': '学生信息表'}

    id: Mapped[int_pk]
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"), nullable=True)
    username: Mapped[required_unique_name]
    password: Mapped[required_string]
    nickname: Mapped[required_string]

    # 定义映射关系
    classroom: Mapped["Classroom"] = relationship(lazy=True, back_populates="students")
    group: Mapped["Group"] = relationship(lazy=True, back_populates="students")
    discussions: Mapped[list["Discussion"]] = relationship(back_populates="creator")
    nodes: Mapped[list["NodeTable"]] = relationship(back_populates="from_student")


class Discussion(Base):
    __tablename__ = 'discussion'
    __table_args__ = {'comment': '讨论信息表'}

    id: Mapped[int_pk]
    topic_content: Mapped[required_string]
    created_time: Mapped[timestamp_default_now]
    created_user_id: Mapped[int] = mapped_column(ForeignKey("student.id"), nullable=False)
    topic_for_class_id: Mapped[int] = mapped_column(ForeignKey("class.id"), nullable=False)

    # 定义与Student和Class表之间的关系
    creator: Mapped["Student"] = relationship(back_populates="discussions")
    related_class: Mapped["Classroom"] = relationship(back_populates="discussions")
    nodes: Mapped[list["NodeTable"]] = relationship(back_populates="from_discussion")


NodeTypeDict = {
    "topic": "topic",
    "idea": "idea",
    "group": "group"
}


class NodeTable(Base):
    __tablename__ = 'node_table'
    __table_args__ = {'comment': '节点信息表'}

    id: Mapped[int_pk]
    type: Mapped[string_128]  # 节点类型 topic or idea or group
    content: Mapped[string_1000]
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), nullable=False)
    topic_id: Mapped[int] = mapped_column(ForeignKey("discussion.id"), nullable=False)
    created_time: Mapped[timestamp_default_now]

    # 定义与Student, Group表, Class表以及Discussion表之间的关系
    from_student: Mapped["Student"] = relationship(back_populates="nodes")
    from_group: Mapped["Group"] = relationship(back_populates="nodes")
    from_classroom: Mapped["Classroom"] = relationship(back_populates="nodes")
    from_discussion: Mapped["Discussion"] = relationship(back_populates="nodes")


EdgeTypeDict = {
    "approve": "approve",
    "reject": "reject",
    "group_to_discuss": "group_to_discuss",
    "idea_to_group": "idea_to_group"
}


class EdgeTable(Base):
    __tablename__ = 'edge_table'
    __table_args__ = {'comment': '边信息表'}

    id: Mapped[int_pk]
    type: Mapped[string_128]  # 边的类型 approve or reject or group_to_discuss or idea_to_group
    source: Mapped[int] = mapped_column(ForeignKey("node_table.id"), nullable=False)
    target: Mapped[int] = mapped_column(ForeignKey("node_table.id"), nullable=False)
    topic_id: Mapped[int] = mapped_column(ForeignKey("discussion.id"), nullable=False)


class NodeReviseRecordTable(Base):
    __tablename__ = 'node_revise_record_table'
    __table_args__ = {'comment': '节点修改记录信息表'}

    id: Mapped[int_pk]
    node_id: Mapped[int] = mapped_column(ForeignKey("node_table.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), nullable=False)
    revise_content: Mapped[string_1000]
    created_time: Mapped[timestamp_default_now]
