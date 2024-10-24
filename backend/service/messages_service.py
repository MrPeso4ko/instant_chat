from typing import Annotated

from fastapi import Depends

from repository.message import MessageRepository
from serializer import UserGet, MessageCreate, MessageGet, MessageCreateDB


class MessagesService:
    def __init__(self, message_repository: Annotated[MessageRepository, Depends()]):
        self.message_repository = message_repository

    async def create_message(self, current_user: UserGet, chat_id: int, message: MessageCreate) -> MessageGet:
        message_db = MessageCreateDB(from_user_id=current_user.id, chat_id=chat_id, **message.model_dump())
        return await self.message_repository.create(message_db)


