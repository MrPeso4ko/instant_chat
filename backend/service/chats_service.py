from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from exc import WrongChatUsers
from repository import ChatRepository
from serializer import UserGet, ChatCreateDB, ChatGet


class ChatsService:
    def __init__(self, chat_repository: Annotated[ChatRepository, Depends()]):
        self.chat_repository = chat_repository

    async def get_chats(self, user_id):
        return await self.chat_repository.get_by_user_id(user_id)

    async def create_chat(self, current_user: UserGet, second_user: UserGet) -> ChatGet:
        if current_user.id == second_user.id:
            raise WrongChatUsers("Chat cannot be created with same user")
        if current_user.id >= second_user.id:
            current_user, second_user = second_user, current_user
        chat = ChatCreateDB(first_user_id=current_user.id, second_user_id=second_user.id)
        try:
            return await self.chat_repository.create(chat)
        except IntegrityError:
            raise WrongChatUsers("Chat already exists")
