import sqlalchemy

engine = sqlalchemy.create_engine("mysql+pymysql://root:123456@localhost:3307/sqlarchdmy_test", echo=True)

# 创建表对象的meta_data 相当于一个存储空间
meta_data = sqlalchemy.MetaData()

person_table = sqlalchemy.Table(
    "person", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(10), nullable=False, unique=True),  # String(10) 就是相当于 varchar(10)
    sqlalchemy.Column("birthday", sqlalchemy.DateTime),  # 生日
    sqlalchemy.Column("address", sqlalchemy.String(255), nullable=True) # 地址
)

department_table = sqlalchemy.Table(
    "department", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False, unique=True)
)

employee_table = sqlalchemy.Table(
    "employee", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("department_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("department.id"), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False)
)