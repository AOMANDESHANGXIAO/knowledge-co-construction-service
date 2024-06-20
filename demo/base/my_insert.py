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
# meta_data.create_all(engine)

# # insert a record
# person_insert = person.insert()
#
# insert_tom = person_insert.values(name="tom")
#
# # 执行插入
# with engine.connect() as conn:
#     result = conn.execute(insert_tom)
#     # 可以拿到id
#     print(result.inserted_primary_key)
#     # 事务模式，需要提交
#     conn.commit()

# 插入多条记录

person_insert = person.insert()
with engine.connect() as conn:
    conn.execute(person_insert, [
        {"name": "Mike"},
        {"name": "jack"},
        {"name": "lucy"},
        {"name": "lily"},
    ])
    conn.commit()


