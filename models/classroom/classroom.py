# classroom有关的模型
from pydantic import BaseModel


class ClassRoomQueryListRequest(BaseModel):
    id: int

