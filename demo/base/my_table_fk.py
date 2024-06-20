from demo.base.db_init import engine
import sqlalchemy

"""
建表代码
"""


meta_data = sqlalchemy.MetaData()

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

# meta_data.create_all(engine)


"""
插入example数据
"""

with engine.connect() as conn:
    conn.execute(department_table.insert(),[
        {"name": "IT"},
        {"name": "HR"},
        {"name": "Finance"},
        {"name": "Marketing"},
        {"name": "Sales"},
        {"name": "Operations"},
        {"name": "Research"},
        {"name": "Legal"},
        {"name": "Administration"},
        {"name": "Customer Service"},
        {"name": "Training"},
        {"name": "Development"},
        {"name": "Quality Assurance"},
        {"name": "Production"},
        {"name": "Logistics"}
    ])

    conn.execute(employee_table.insert(), [
        {"department_id": 1, "name": "John Doe"},
        {"department_id": 1, "name": "Jane Doe"},
        {"department_id": 2, "name": "Mike Smith"},
        {"department_id": 2, "name": "Amy Jones"},
        {"department_id": 3, "name": "Bob Brown"},
        {"department_id": 3, "name": "Sue Green"},
        {"department_id": 4, "name": "Tom Wilson"},
    ])

    conn.commit()