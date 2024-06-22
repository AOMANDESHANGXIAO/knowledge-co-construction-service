from models.common.common import response_success, response_fail, CommonResponse
from models.table_def import Classroom
from db.session import SessionLocal


def query_classroom_list() -> CommonResponse:
    """
    查询班级列表的方法
    """
    try:
        session = SessionLocal()
        classroom_list = session.query(Classroom).all()

        result = []

        for row in classroom_list:
            result.append({
                "id": row.id,
                "class_name": row.class_name
            })

        return response_success(data={"list": result})
    except Exception as e:
        return response_fail(message=str(e))

