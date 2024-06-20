# 导入sqlalchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.table_def import Student

# 如果你还没有定义ORM模型，可以这样定义一个简单的User模型
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# 数据库地址
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3307/knowledgebuilding"
# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
# 创建一个session类，用于数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 用于构建数据类型
Base = declarative_base()

# 使用完了关闭引擎
engine.dispose()
