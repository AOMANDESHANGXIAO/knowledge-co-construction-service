# 使用mapped 映射类
import datetime
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy.sql import func

from typing_extensions import Annotated

# 定义类型，方便复用
int_pk = Annotated[int, mapped_column(primary_key=True)]
required_unique_name = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]
timestamp_default_now = Annotated[datetime.datetime, mapped_column(nullable=False, server_default=func.now())]  #
# serve_default相当于指定sql语句的默认值 需要在建表的时候就写上

engine = create_engine("mysql+pymysql://root:123456@localhost:3307/sqlalchemy_map_testdb", echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Department(Base):
    __tablename__ = "department"

    id: Mapped[int_pk]
    name: Mapped[required_unique_name]
    create_time: Mapped[timestamp_default_now]

    # list里面要写引用
    employees: Mapped[list["Employee"]] = relationship(lazy=True, back_populates="departments")

    """
        方便打印
    """

    def __repr__(self):
        return f"Department(id={self.id!r}, name={self.name!r}, create_time={self.create_time!r})"


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int_pk]
    dep_id: Mapped[int] = mapped_column(ForeignKey("department.id"))
    name: Mapped[required_unique_name]
    birthday: Mapped[datetime.datetime] = mapped_column(nullable=False)

    # 并非数据库中的字段，而是一种关系的映射
    # backref 表示反向关系，即通过department属性访问employee
    # 第一种方式，在Department中不需要进行定义
    # department: Mapped[Department] = relationship(lazy=True, backref="employee")
    # 第二种方式, 在Department中定义
    departments: Mapped[Department] = relationship(lazy=True, back_populates="employees")

    def __repr__(self):
        return f"Employee(id={self.id!r}, name={self.name!r}, birthday={self.birthday!r})"


# 创建表
Base.metadata.create_all(engine)
