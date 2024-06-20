from db_init import Session, Person

# 开启事务
session = Session()


# 单条修改方式一
# person = session.query(Person).filter(Person.id == 1).one()
#
# person.name = "Jack"

# 单条修改方式二
session.query(Person).filter(Person.id == 2).update({Person.address: "Beijing", Person.name: "Tom"})


# 提交事务
session.commit()
