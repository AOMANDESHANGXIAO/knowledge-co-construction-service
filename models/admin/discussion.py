from pydantic import BaseModel


class CreateDiscussionParams(BaseModel):
    topic_content: str
    class_id: int
    created_user_id: int
