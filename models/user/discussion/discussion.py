from pydantic import BaseModel
from datetime import datetime


class DiscussionQueryDataItem(BaseModel):
    id: int
    topic_content: str
    created_time: datetime
    created_user_name: str
