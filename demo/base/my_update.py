from demo.base.db_init import engine, person_table

with engine.connect() as conn:
    # 更新所有地址为New York
    # update_query = person_table.update().values(address="New York")
    # 按条件更新
    update_query = person_table.update().values(address="Bei Jing").where(person_table.c.id < 3)
    # 更新操作不返回结果
    conn.execute(update_query)
    conn.commit()
