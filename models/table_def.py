from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.annotated_type import int_pk, required_unique_name, required_string, timestamp_default_now

Base = declarative_base()


class Classroom(Base):
    __tablename__ = 'class'
    __table_args__ = {'comment': '班级信息表'}

    id: Mapped[int_pk]
    class_name: Mapped[required_unique_name]

    students: Mapped[list["Student"]] = relationship(back_populates="classroom")
    discussions: Mapped[list["Discussion"]] = relationship(back_populates="related_class")
    groups: Mapped[list["Group"]] = relationship(lazy=True, back_populates="belong_classroom")


class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'comment': '协作团队信息表'}

    id: Mapped[int_pk]
    group_name: Mapped[required_unique_name]
    group_description: Mapped[required_string]
    group_code: Mapped[required_unique_name]
    belong_class_id: Mapped[int] = mapped_column(ForeignKey("class.id"), nullable=True)

    belong_classroom: Mapped["Classroom"] = relationship(lazy=True, back_populates="groups")
    students: Mapped[list["Student"]] = relationship(lazy=True, back_populates="group")


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
