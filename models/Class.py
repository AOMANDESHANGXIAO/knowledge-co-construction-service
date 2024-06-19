from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Classroom(Base):
    __tablename__ = 'class'
    __table_args__ = {'comment': '班级信息表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="班级的id", nullable=False)
    class_name = Column(String[10], comment="班级的名称", nullable=False)

