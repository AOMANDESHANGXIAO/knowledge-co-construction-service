from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.table_def import Student, Classroom, Group, Discussion

engine = create_engine("mysql+pymysql://root:123456@localhost:3307/knowledgebuilding", echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()


def test_query_student():
    result = session.query(Student)

    for row in result:
        print(row.username)


def test_query_classroom():
    result = session.query(Classroom)
    for row in result:
        print(row.class_name, row.id)


def test_query_classroom_student():
    query_class = session.query(Classroom).filter(Classroom.id == 1).one()

    for student in query_class.students:
        print(student.username)


def test_query_discussion():
    result = session.query(Discussion)
    for row in result:
        print(row.topic_content)


test_query_discussion()
