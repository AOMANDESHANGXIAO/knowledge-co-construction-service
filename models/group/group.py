from pydantic import BaseModel


class GroupCreateParams(BaseModel):
    group_name: str
    group_description: str
    class_id: int
    group_color: str
