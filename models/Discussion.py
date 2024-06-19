from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Discussion(Base):
    __tablename__ = 'discussion'
    __table_args__ = {'comment': '讨论信息表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="讨论话题的id")
    topic_content = Column(String(50), nullable=False, comment="讨论话题的内容")
    created_time = Column(DateTime, nullable=False, comment="创建时间")
    created_user_id = Column(Integer, ForeignKey('student.id'), nullable=False, comment="创建讨论话题的用户")
    topic_for_class_id = Column(Integer, ForeignKey('class.id'), nullable=False, comment="关联的班级id")

    # 定义与Student和Class表之间的关系
    creator = relationship("student", backref="discussions_created", foreign_keys=[created_user_id])
    related_class = relationship("class", backref="related_discussions", foreign_keys=[topic_for_class_id])

