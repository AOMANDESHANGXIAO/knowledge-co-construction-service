from db_init import Session, Person

session = Session()

p = Person(name="John Doe", birthday="1980-01-01", address="123 Main St.")

# 添加单条记录
# session.add(p)

# 添加多条记录
session.add_all([
    Person(name="Elizabeth Doe", birthday="1985-02-02", address="456 Other St."),
    Person(name="Jim Doe", birthday="1990-03-03", address="789 Anywhere St.")
])


session.commit()
