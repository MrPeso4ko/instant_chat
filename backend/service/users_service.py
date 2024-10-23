from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.exc import NoResultFound
from watchfiles import awatch

from exc import UserNotFound
from repository import UserRepository
from serializer import UserGet


class UsersService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]):
        self.user_repository = user_repository

    async def get_by_name(self, name: str) -> UserGet:
        try:
            return await self.user_repository.get_by_name(name)
        except NoResultFound:
            raise UserNotFound
