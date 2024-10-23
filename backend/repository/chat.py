from sqlalchemy import select, or_

from model import Chat
from repository.base import BaseRepository
from serializer import ChatCreateDB, ChatGet


class ChatRepository(BaseRepository):
    model = Chat

    async def create(self, chat: ChatCreateDB) -> ChatGet:
        return ChatGet.model_validate(await super(ChatRepository, self).create(chat))

    async def get_by_user_id(self, user_id: int) -> list[ChatGet]:
        query = select(self.model).where(or_(self.model.first_user_id == user_id, self.model.second_user_id == user_id))
        res = await self.session.execute(query)
        return [ChatGet.model_validate(chat) for chat in res.scalars().all()]

    # async def get_by_username(self, username: str) -> UserGetDB:
    #     query = select(self.model).where(self.model.username == username)
    #     res = await self.session.execute(query)
    #     return UserGetDB.model_validate(res.scalar_one())
