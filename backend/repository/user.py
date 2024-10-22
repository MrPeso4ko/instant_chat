from sqlalchemy import select

from model import User
from repository.base import BaseRepository
from serializer import UserGet, UserCreateDB, UserGetDB


class UserRepository(BaseRepository):
    model = User

    async def create(self, user: UserCreateDB) -> UserGet:
        return UserGet.model_validate(await super(UserRepository, self).create(user))

    async def get_by_id(self, user_id: int) -> UserGet:
        return UserGet.model_validate(await super(UserRepository, self).get_by_id(user_id))

    async def get_by_username(self, username: str) -> UserGetDB:
        query = select(self.model).where(self.model.username == username)
        res = await self.session.execute(query)
        return UserGetDB.model_validate(res.scalar_one())
