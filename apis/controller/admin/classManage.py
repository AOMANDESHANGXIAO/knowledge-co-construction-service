from models.table_def import Classroom
from models.common.common import CommonResponse, response_success, response_fail
from models.admin.classManage import CreateClassParams, DropClassParams
from db.session import SessionLocal


def create_class(params: CreateClassParams) -> CommonResponse:
    session = SessionLocal()
    try:
        new_class = Classroom(class_name=params.class_name)
        session.add(new_class)
        session.commit()
        return response_success(message="创建成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def drop_class(params: DropClassParams) -> CommonResponse:
    session = SessionLocal()

    try:
        session.query(Classroom).filter(Classroom.id == params.class_id).update({"status": 0})

        session.commit()

        return response_success(message="删除成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def query_class_list() -> CommonResponse:
    session = SessionLocal()
    try:
        class_list = session.query(Classroom).filter(Classroom.status == 1).all()
        class_list = [{"class_id": class_item.id, "class_name": class_item.class_name} for class_item in class_list]

        return response_success(data={"list": class_list})
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()
