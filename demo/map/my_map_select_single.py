# 通过映射来查询
from db_init import Session, Person

session = Session()
# 相当于select * from person
# result = session.query(Person).all()

# 只拿第一条记录 first()
# result = session.query(Person).filter(Person.birthday > '1985-01-01').first()
# 使用first()时result不能为空

# 必须查出来的有且只有一条 one()
# result = session.query(Person).filter(Person.id == 1).one()

# 可以查出来为空 scalar(), 但是也不能查多条
result = session.query(Person).filter(Person.id == 1).scalar()

print(result.name)

