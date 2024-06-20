from demo.base.db_init import engine, person_table
from sqlalchemy.sql import and_, or_

with engine.connect() as conn:
    # query = person_table.select().where(person_table.c.id < 3)

    # 复杂查询条件
    query = person_table.select().where(
        or_(
            person_table.c.name == 'tom',
            and_(
                person_table.c.birthday > '2024-06-05',
                person_table.c.id < 7
            )
        )
    )

    result_set = conn.execute(query)

    for row in result_set:
        print(row.id, row.name, row.birthday)
