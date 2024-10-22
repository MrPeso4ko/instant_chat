import re
from typing import Annotated

from fastapi import Depends, Request
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError, NoResultFound

from exc import UserAlreadyExists, IncorrectPassword, UserNotFound, SessionNotFound
from repository import UserRepository
from serializer import UserCreate, UserGet, UserCreateDB, UserAuth
from service.session_manager import SessionManager

from util.passwords import hash_password, check_password


class AuthService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()],
                 session_manager: Annotated[SessionManager, Depends()]):
        self.user_repository = user_repository
        self.session_manager = session_manager

    async def register_user(self, request: Request, user: UserCreate) -> JSONResponse:
        hashed_password, salt = hash_password(user.password)

        user_db = UserCreateDB(name=user.name, username=user.username, hashed_password=hashed_password, salt=salt)
        try:
            user = await self.user_repository.create(user_db)
            return await self.successful_response(request, user.id)
        except IntegrityError as e:
            matches = re.findall(r"\((.+)\)=\((.+)\)", str(e))
            if not matches or len(matches) > 1:
                raise e
            arg, value = matches[0]
            raise UserAlreadyExists(arg, value)

    async def check_auth(self, request: Request, user: UserAuth) -> JSONResponse:
        try:
            user_db = await self.user_repository.get_by_username(user.username)
        except NoResultFound as e:
            raise UserNotFound(e)

        if check_password(user.password, user_db.hashed_password, user_db.salt):
            return await self.successful_response(request, user_db.id)
        else:
            raise IncorrectPassword()

    async def successful_response(self, request: Request, user_id: int):
        response = JSONResponse({"status": "success"}, status_code=200)
        session_id = await self.session_manager.create_session(user_id=user_id)
        response.set_cookie(key="session_id",
                            value=session_id,
                            # httponly=True,
                            domain=request.base_url.hostname,
                            max_age=60 * 60 * 24 * 30,)
        return response

    async def get_me(self, session_id: str | None) -> UserGet:
        if not session_id:
            raise SessionNotFound()
        user_id = await self.session_manager.get_user_id(session_id)
        if not user_id:
            raise SessionNotFound()
        user = await self.user_repository.get_by_id(user_id)
        return user
