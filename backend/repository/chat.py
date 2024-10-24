from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload

from model import Chat
from repository.base import BaseRepository
from serializer import ChatCreateDB, ChatGet
from serializer import ChatGetExtended


class ChatRepository(BaseRepository):
    model = Chat

    async def create(self, chat: ChatCreateDB) -> ChatGet:
        return ChatGet.model_validate(await super(ChatRepository, self).create(chat))

    async def get_by_user_id(self, user_id: int) -> list[ChatGet]:
        query = select(self.model).where(or_(self.model.first_user_id == user_id, self.model.second_user_id == user_id))
        res = await self.session.execute(query)
        return [ChatGet.model_validate(chat) for chat in res.scalars().all()]

    async def get_by_id(self, chat_id: int) -> ChatGetExtended:
        query = select(self.model).where(self.model.id == chat_id).options(joinedload(Chat.messages))
        res = await self.session.execute(query)
        return ChatGetExtended.model_validate(res.unique().scalar_one())
