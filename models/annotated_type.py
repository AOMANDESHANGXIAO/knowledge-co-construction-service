import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

# 定义类型，方便复用
int_pk = Annotated[int, mapped_column(primary_key=True)]

required_unique_name = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]

required_string = Annotated[str, mapped_column(String(128), nullable=False)]

string_255 = Annotated[str, mapped_column(String(255), nullable=True)]

timestamp_default_now = Annotated[datetime.datetime, mapped_column(nullable=False, server_default=func.now())]  #
# serve_default相当于指定sql语句的默认值 需要在建表的时候就写上
