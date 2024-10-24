from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseMessage(BaseModel):
    from_user_id: int
    chat_id: int
    text: str


class MessageGet(BaseMessage):
    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime
