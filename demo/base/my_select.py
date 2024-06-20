from demo.base.db_init import engine, person_table

with engine.connect() as conn:
    query = person_table.select()
    # 拿到一个结果集，实质上是一个迭代器
    result_set = conn.execute(query)

    # # 返回的实质上是元组
    # for row in result_set:
    #     # 方式1
    #     print(row.id, row.name)
    #     # 方式2
    #     print(row[0], row[1])

    # 另一个做法，fetchall(), 在结果不算多的时候可以这么干
    # 返回以元组作为元素的列表
    result = result_set.fetchall()
    print(result)
