from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseMessage(BaseModel):
    text: str


class MessageCreate(BaseMessage):
    pass


class MessageCreateDB(MessageCreate):
    from_user_id: int
    chat_id: int


class MessageGet(BaseMessage):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_user_id: int
    chat_id: int

    created_at: datetime
