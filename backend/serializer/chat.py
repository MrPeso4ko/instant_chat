from pydantic import BaseModel, ConfigDict

from serializer.user import BaseUserGet
from serializer.message import MessageGet


class BaseChat(BaseModel):
    first_user: BaseUserGet
    second_user: BaseUserGet


class ChatGet(BaseChat):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ChatGetExtended(ChatGet):
    messages: list[MessageGet]


class ChatDB(BaseModel):
    first_user_id: int
    second_user_id: int


class ChatCreateDB(ChatDB):
    pass
