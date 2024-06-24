from pydantic import BaseModel


class GroupCreateParams(BaseModel):
    student_id: int
    group_name: str
    group_description: str
    class_id: int
    group_color: str


class GroupJoinParams(BaseModel):
    student_id: int
    group_code: str


# "group_id": new_group.id,
# "group_name": new_group.group_name,
# "group_description": new_group.group_description,
# "group_code": new_group.group_code,
# "group_color": new_group.group_color,
# "belong_class_id": new_group.belong_class_id,
class GroupInfo(BaseModel):
    group_id: int
    group_name: str
    group_description: str
    group_code: str
    group_color: str
    belong_class_id: int
