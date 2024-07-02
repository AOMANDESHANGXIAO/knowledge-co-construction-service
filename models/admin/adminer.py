from pydantic import BaseModel


class AdminerSignInParams(BaseModel):
    username: str
    password: str


class AdminerSignInResponse(BaseModel):
    token: str
    nickname: str
    id: int


class AdminerSignUpParams(BaseModel):
    username: str
    password: str
    nickname: str
