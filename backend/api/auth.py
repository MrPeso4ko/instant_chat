from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from exc import UserAlreadyExists, UserNotFound, IncorrectPassword
from serializer import UserGet
from serializer.user import UserCreate, UserAuth
from service import AuthService

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/register")
async def register_user(user: UserCreate, auth_service: Annotated[AuthService, Depends()]) -> UserGet:
    try:
        return await auth_service.register_user(user)
    except UserAlreadyExists:
        raise HTTPException(400, "User with this name or username already exists")


@auth_router.post("/login")
async def log_in(auth_data: UserAuth, auth_service: Annotated[AuthService, Depends()]) -> UserGet:
    try:
        user = await auth_service.check_auth(auth_data)
        return user
    except UserNotFound:
        raise HTTPException(404, "User not found")
    except IncorrectPassword:
        raise HTTPException(401, "Incorrect password")
