import sqlalchemy

engine = sqlalchemy.create_engine("mysql+pymysql://root:123456@localhost:3307/sqlarchdmy_test", echo=True)

# 创建表对象的meta_data 相当于一个存储空间
meta_data = sqlalchemy.MetaData()

person = sqlalchemy.Table(
    "person", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(10), nullable=False, unique=True)  # String(10) 就是相当于 varchar(10)
)

# 构建
meta_data.create_all(engine)

# 使用完了关闭引擎
engine.dispose()
