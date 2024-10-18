from typing import Annotated

from fastapi.params import Depends

from sqlalchemy.exc import IntegrityError, NoResultFound

from exc import UserAlreadyExists, IncorrectPassword, UserNotFound
from repository import UserRepository
from serializer import UserCreate, UserGet, UserCreateDB, UserAuth

from util.passwords import hash_password, check_password


class AuthService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]):
        self.user_repository = user_repository

    async def register_user(self, user: UserCreate) -> UserGet:
        hashed_password, salt = hash_password(user.password)

        user_db = UserCreateDB(name=user.name, username=user.username, hashed_password=hashed_password, salt=salt)
        try:
            user = await self.user_repository.create(user_db)
            return user
        except IntegrityError as e:
            raise UserAlreadyExists(e)

    async def check_auth(self, user: UserAuth) -> UserGet:
        try:
            user_db = await self.user_repository.get_by_username(user.username)
        except NoResultFound as e:
            raise UserNotFound(e)

        if check_password(user.password, user_db.hashed_password, user_db.salt):
            return UserGet.model_validate(user_db)
        else:
            raise IncorrectPassword()
