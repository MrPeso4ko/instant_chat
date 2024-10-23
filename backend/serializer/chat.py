from pydantic import BaseModel, ConfigDict

from serializer import BaseUserGet


class BaseChat(BaseModel):
    first_user: BaseUserGet
    second_user: BaseUserGet


class ChatGet(BaseChat):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ChatDB(BaseModel):
    first_user_id: int
    second_user_id: int


class ChatCreateDB(ChatDB):
    pass
