# 导入sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.Student import Student

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


# 创建简单的测试
class Class(Base):
    __tablename__ = "Class"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    class_name = Column(String[10], nullable=False)


# 使用session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 示例：使用session执行查询
def query_users():
    db = next(get_db())
    users = db.query(Class).all()  # 假设User是定义好的ORM模型
    for user in users:
        print(user.class_name, user.id)


def query_students():
    db = next(get_db())
    students = db.query(Student).all()
    for student in students:
        print(student.username, student.id)


# query_users()
query_students()
