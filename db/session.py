# 导入sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import CONFIG

# 数据库地址
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{CONFIG['USER']}:{CONFIG['PASSWORD']}@{CONFIG['HOST']}:{CONFIG['PORT']}/{CONFIG['DATABASE']}"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# 创建一个session类，用于数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


