from models.group.group import GroupCreateParams, GroupJoinParams
from models.common.common import CommonResponse, response_success, response_fail
from db.session import SessionLocal
from models.table_def import Group, Student


def create_group(params: GroupCreateParams) -> CommonResponse:
    session = SessionLocal()
    try:
        # 查询创建团队的学生是否已经有团队了，有的话就拒绝创建
        db_student = session.query(Student).filter(Student.id == params.student_id).first()
        if db_student.group_id:
            print("the group_id =", db_student.group_id)
            return response_fail(message="该学生已经有团队了")

        # 组名不能重复
        db_group = session.query(Group).filter(Group.group_name == params.group_name).first()

        if db_group:
            return response_fail(message="组名重复")

        # 否则插入一个组到数据库
        new_group = Group(
            **{
                "group_name": params.group_name,
                "group_description": params.group_description,
                "belong_class_id": params.class_id,
                "group_color": params.group_color
            }
        )
        # 要拿到新插入数据的主键
        session.add(new_group)
        session.flush()
        session.refresh(new_group)  # 刷新数据才能拿到主键

        # 为团队生成团队码，格式为: ckc+id
        session.query(Group).filter(Group.id == new_group.id).update({"group_code": f"ckc{new_group.id}"})

        # 更新创建团队的学生的group_id
        session.query(Student).filter(Student.id == params.student_id).update({"group_id": new_group.id})

        session.commit()

        data = {
            "group_id": new_group.id,
            "group_name": new_group.group_name,
            "group_description": new_group.group_description,
            "group_code": new_group.group_code,
            "group_color": new_group.group_color,
            "belong_class_id": new_group.belong_class_id,
        }

        return response_success(message="创建成功", data=data)
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def join_group(params: GroupJoinParams) -> CommonResponse:
    session = SessionLocal()
    try:
        db_group = session.query(Group).filter(Group.group_code == params.group_code)

        if not db_group:
            return response_fail(message="团队不存在")

        db_student = session.query(Student).filter(Student.id == params.student_id).first()

        if db_student.group_id:
            return response_fail(message="该学生已在团队中")

        session.query(Student).filter(Student.id == params.student_id).update({"group_id": db_group.id})

        return response_success(data={
            "group_id": db_group.id,
            "group_name": db_group.group_name,
            "group_description": db_group.group_description,
            "group_code": db_group.group_code,
            "group_color": db_group.group_color,
            "belong_class_id": db_group.belong_class_id,
        }, message="加入成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def query_student_group(student_id: int) -> CommonResponse:
    session = SessionLocal()
    try:
        db_student = session.query(Student).filter(Student.id == student_id).first()
        if not db_student.group_id:
            return response_fail(message="该学生没有团队")

        db_group = db_student.group

        return response_success(data={
            "group_id": db_group.id,
            "group_name": db_group.group_name,
            "group_description": db_group.group_description,
            "group_code": db_group.group_code,
            "group_color": db_group.group_color,
            "belong_class_id": db_group.belong_class_id,
        })
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


# ======================================================
def test_create_group() -> CommonResponse:
    params = GroupCreateParams(
        group_name="test_group4",
        group_description="test_group_description",
        class_id=1,
    )
    return create_group(params)


def test_query_student_group() -> CommonResponse:
    params = GroupQueryParams(
        student_id=1
    )
    return query_student_group(params)

# print(test_query_student_group())
# print(test_create_group())
