from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'comment': '协作团队信息表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="学生的id", nullable=False)
    group_name = Column(String[10], comment="所属团队的id", nullable=False)
    group_description = Column(String[100], comment="团队的描述", nullable=False)


class Classroom(Base):
    __tablename__ = 'class'
    __table_args__ = {'comment': '班级信息表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="班级的id", nullable=False)
    class_name = Column(String[10], comment="班级的名称", nullable=False)


class Student(Base):
    __tablename__ = 'student'
    __table_args__ = {'comment': '学生信息表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="学生的id")
    group_id = Column(Integer, ForeignKey("group.id"), comment="所属团队的id")
    class_id = Column(Integer, ForeignKey("class.id"), nullable=False, comment="所属班级的id")
    username = Column(String(10), nullable=False, unique=True, comment="账号")
    password = Column(String(10), nullable=False, comment="密码")
    nickname = Column(String(10), nullable=False, comment="昵称")

    # 定义与Group和Class表之间的关系（如果它们也被映射为ORM模型）
    # 假设Group和Class类已经定义
    group = relationship("Group", foreign_keys=[group_id])
    _class = relationship("Classroom", foreign_keys=[class_id])
