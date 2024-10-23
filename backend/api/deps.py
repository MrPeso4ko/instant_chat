from typing import Annotated

from fastapi import HTTPException, Depends, Cookie

from exc import SessionNotFound, UserNotFound
from serializer import UserGet
from service import AuthService
from service.users_service import UsersService


async def get_current_user(auth_service: Annotated[AuthService, Depends()], session_id: Annotated[str, Cookie()] = "", ) -> UserGet:
    try:
        return await auth_service.get_me(session_id)
    except SessionNotFound as e:
        raise HTTPException(401, "Unauthorized")


async def get_user_by_name(name: str, users_service: Annotated[UsersService, Depends()]) -> UserGet:
    try:
        return await users_service.get_by_name(name)
    except UserNotFound:
        raise HTTPException(404, f"User with name {name} not found")
