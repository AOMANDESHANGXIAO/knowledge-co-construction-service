# 通过映射来查询
from db_init import Session, Person

session = Session()
# 相当于select * from person
# result = session.query(Person).all()

# 简单条件查询
result = session.query(Person).filter(Person.birthday > '1985-01-01')


for person in result:
    print(person.name, person.birthday)



