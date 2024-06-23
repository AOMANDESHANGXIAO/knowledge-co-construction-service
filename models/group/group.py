from pydantic import BaseModel


class GroupCreateParams(BaseModel):
    student_id: int
    group_name: str
    group_description: str
    class_id: int
    group_color: str


class GroupQueryParams(BaseModel):
    student_id: int
