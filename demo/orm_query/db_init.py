from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, relationship
import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

# 定义类型，方便复用
int_pk = Annotated[int, mapped_column(primary_key=True)]

required_unique_name = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]

required_string = Annotated[str, mapped_column(String(128), nullable=False)]

timestamp_default_now = Annotated[datetime.datetime, mapped_column(nullable=False, server_default=func.now())]  #
# serve_default相当于指定sql语句的默认值 需要在建表的时候就写上

Base = declarative_base()


class Department(Base):
    __tablename__ = "department"

    id: Mapped[int_pk]
    name: Mapped[required_unique_name]

    employees: Mapped[list["Employee"]] = relationship(lazy=True, back_populates="department")

    def __repr__(self) -> str:
        return f"<Department(id={self.id}, name={self.name})>"


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int_pk]
    department_id: Mapped[int] = mapped_column(ForeignKey("department.id"))
    name: Mapped[required_string]

    department: Mapped[Department] = relationship(lazy=True, back_populates="employees")

    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, name={self.name})>"


engine = create_engine("mysql+pymysql://root:123456@localhost:3307/sqlarchdmy_test", echo=True)

Session = sessionmaker(bind=engine)

session = Session()


def query_department(s: Session):
    department = s.query(Department).filter(Department.id == 1).first()
    print(department.name)


def select_multiple(s: Session):
    # q = select(Department).order_by(Department.name)
    q = select(Department, Employee).join(Employee.department).filter(Department.id == 1)
    res = s.execute(q)

    for row in res:
        print(row)


select_multiple(session)
