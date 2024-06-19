from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'comment': '协作团队信息表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="学生的id", nullable=False)
    group_name = Column(String[10], comment="所属团队的id", nullable=False)
    group_description = Column(String[100], comment="团队的描述", nullable=False)

