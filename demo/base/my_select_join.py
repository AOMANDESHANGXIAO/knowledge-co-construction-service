from demo.base.db_init import engine, department_table, employee_table
import sqlalchemy


with engine.connect() as conn:
    # 将员工和部门表进行连接
    join = employee_table.join(department_table, department_table.c.id == employee_table.c.department_id)
    # query = sqlalchemy.select(join).where(department_table.c.name == 'Manage')
    # 不需要部门信息
    query = sqlalchemy.select(employee_table).select_from(join).where(department_table.c.name == 'Manage')
    result_set = conn.execute(query).fetchall()

    print(result_set)