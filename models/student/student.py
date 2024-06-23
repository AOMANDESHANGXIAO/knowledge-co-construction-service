from pydantic import BaseModel


class Student(BaseModel):
    group_id: str = None
    group_code: str = None
    class_id: int = None
    username: str
    password: str
    nickname: str


class StudentSignUp(BaseModel):
    username: str
    password: str
    nickname: str
    class_id: int


class StudentSignIn(BaseModel):
    username: str
    password: str
