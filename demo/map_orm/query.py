from db_init import Session, Department, Employee


def insert_records(session: Session):
    d1 = Department(name="hr")
    session.add(d1)
    # 强行刷新缓存，但是消耗性能，不建议这么做
    session.flush()

    e1 = Employee(name="Jack", birthday="1990-01-01", dep_id=d1.id)
    session.add(e1)

    session.commit()


def select_employee(session: Session):
    emp = session.query(Employee).filter(Employee.id == 1).one()
    print(emp)
    print(emp.department)  # 通过关系直接查部门, 默认是lazy


def select_department(session: Session):
    dep = session.query(Department).filter(Department.id == 1).one()

    print(dep)

    # 根据部门直接查员工
    print(dep.employees)


session = Session()

select_department(session)
