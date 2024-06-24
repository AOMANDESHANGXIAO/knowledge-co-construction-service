from models.student.student import StudentSignUp, StudentSignIn, StudentInfo
from db.session import SessionLocal
from models.table_def import Student
from models.common.common import CommonResponse, response_success, response_fail
from utils.psd_handler import hash_password, verify_password
from utils.jwt_handler import create_access_token


def student_sign_up(params: StudentSignUp) -> CommonResponse:
    """
    处理学生注册接口函数
    """
    session = SessionLocal()
    try:
        db_student = session.query(Student).filter(Student.username == params.username).first()

        if db_student:
            return response_fail(message="用户名已存在")

        new_student = Student(
            **params.dict()
        )

        new_student.password = hash_password(new_student.password)

        session.add(new_student)
        session.commit()

        return response_success(message="注册成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def student_sign_in(params: StudentSignIn) -> CommonResponse:
    """
    处理学生登录接口函数
    """
    session = SessionLocal()
    try:
        db_student = session.query(Student).filter(Student.username == params.username).first()

        if not db_student:
            return response_fail(message="用户名不存在")

        if not verify_password(params.password, db_student.password):
            return response_fail(message="密码错误")

        # 将用户信息带回给前端
        data = StudentInfo(**{
            "id": db_student.id,
            "username": db_student.username,
            "nickname": db_student.nickname,
            "class_id": db_student.class_id,
            "group_id": db_student.group_id,
            "token": create_access_token(data={"username": db_student.username})
        }).__dict__

        return response_success(message="登录成功", data=data)
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def test_student_sign_up():
    """
    测试学生注册接口函数
    """
    params = StudentSignUp(username="qeqweqw", password="test", nickname="test", class_id=1)
    result = student_sign_up(params)
    print(result)


def test_student_sign_in():
    """
    测试学生登录接口函数
    """
    params = StudentSignIn(username="qeqweqw", password="test")
    result = student_sign_in(params)
    print(result)


# test_student_sign_up()
# test_student_sign_in()
