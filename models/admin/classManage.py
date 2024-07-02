from pydantic import BaseModel


class CreateClassParams(BaseModel):
    class_name: str


class DropClassParams(BaseModel):
    class_id: int
