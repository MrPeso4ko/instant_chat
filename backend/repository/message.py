from model import Message
from repository.base import BaseRepository
from serializer import MessageGet, MessageCreateDB


class MessageRepository(BaseRepository):
    model = Message

    async def create(self, message: MessageCreateDB) -> MessageGet:
        return MessageGet.model_validate(await super(MessageRepository, self).create(message))
