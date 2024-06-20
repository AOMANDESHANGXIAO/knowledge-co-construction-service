# 使用mapped 映射类
import datetime
from sqlalchemy import create_engine, String, ForeignKey, Column, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy.sql import func

from typing_extensions import Annotated

# 定义类型，方便复用
int_pk = Annotated[int, mapped_column(primary_key=True)]
required_unique_name = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]
required_string = Annotated[str, mapped_column(String(128), nullable=False)]
timestamp_default_now = Annotated[datetime.datetime, mapped_column(nullable=False, server_default=func.now())]  #
# serve_default相当于指定sql语句的默认值 需要在建表的时候就写上


Base = declarative_base()

# 关联关系表
association_table = Table(
    "association_table", Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True)
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int_pk]
    name: Mapped[required_unique_name]
    password: Mapped[required_string]

    roles: Mapped[list["Role"]] = relationship(secondary=association_table, back_populates="users")

    def __repr__(self) -> str:
        return f"<User(name={self.name!r})>"


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int_pk]
    name: Mapped[required_unique_name]

    def __repr__(self) -> str:
        return f"<Role(name={self.name!r})>"


engine = create_engine("mysql+pymysql://root:123456@localhost:3307/sqlalchemy_map_testdb", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bing=engine)
