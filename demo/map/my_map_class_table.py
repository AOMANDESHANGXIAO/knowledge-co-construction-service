# 使用映射类来定义表
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:123456@localhost:3307/sqlalchemy_map_testdb", echo=True)

Base = declarative_base()


# 使用类来映射表
class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    birthday = Column(DateTime, nullable=True)
    address = Column(String(255), nullable=True)


# 构建表
Base.metadata.create_all(engine)
