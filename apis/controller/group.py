from models.group.group import GroupCreateParams
from models.common.common import CommonResponse, response_success, response_fail
from db.session import SessionLocal
from models.table_def import Group


def create_group(params: GroupCreateParams) -> CommonResponse:
    session = SessionLocal()
    try:
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

        session.commit()

        data = {
            "group_id": new_group.id,
            "group_name": new_group.group_name,
            "group_description": new_group.group_description,
            "group_code": new_group.group_code,
            "belong_class_id": new_group.belong_class_id,
        }

        return response_success(message="创建成功", data=data)
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def test_create_group() -> CommonResponse:
    params = GroupCreateParams(
        group_name="test_group4",
        group_description="test_group_description",
        class_id=1,
    )
    return create_group(params)


# print(test_create_group())
