# classroom有关的模型
from pydantic import BaseModel


class ClassroomQueryDataItem(BaseModel):
    id: int
    class_name: str
