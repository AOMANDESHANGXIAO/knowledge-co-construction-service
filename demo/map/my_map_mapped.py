# 使用mapped 映射类
import datetime
from sqlalchemy import create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy.sql import func

from typing_extensions import Annotated

# 定义类型，方便复用
int_pk = Annotated[int, mapped_column(primary_key=True)]
required_unique_name = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]
timestamp_default_now = Annotated[datetime.datetime, mapped_column(nullable=False, server_default=func.now())]  #
# serve_default相当于指定sql语句的默认值 需要在建表的时候就写上

engine = create_engine("mysql+pymysql://root:123456@localhost:3307/sqlalchemy_map_testdb", echo=True)
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int_pk]
    name: Mapped[required_unique_name]
    # name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    birthday: Mapped[datetime.datetime]
    create_time: Mapped[timestamp_default_now]


# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
