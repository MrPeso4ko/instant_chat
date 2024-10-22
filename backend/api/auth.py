from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Cookie

from common.response_model import status_model, exception_model
from exc import UserAlreadyExists, UserNotFound, IncorrectPassword, SessionNotFound
from serializer import UserGet
from serializer.user import UserCreate, UserAuth
from service import AuthService

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/register", responses={200: status_model("ok"),
                                          400: exception_model("User with name/username [NAME/USERNAME] already exists")})
async def register_user(request: Request, user: UserCreate, auth_service: Annotated[AuthService, Depends()]):
    try:
        return await auth_service.register_user(request, user)
    except UserAlreadyExists as e:
        raise HTTPException(400, f"User with {e.arg} \"{e.value}\" already exists")


@auth_router.post("/login", responses={200: status_model("ok"),
                                       404: exception_model("User not found"),
                                       401: exception_model("Incorrect password or username"), })
async def log_in(request: Request, auth_data: UserAuth, auth_service: Annotated[AuthService, Depends()]):
    try:
        response = await auth_service.check_auth(request, auth_data)
        return response
    except UserNotFound:
        raise HTTPException(404, "User not found")
    except IncorrectPassword:
        raise HTTPException(401, "Incorrect password or username")

@auth_router.get("/get_me", responses={401: exception_model("Unauthorized")})
async def get_me(auth_service: Annotated[AuthService, Depends()], session_id: Annotated[str, Cookie()] = "", ) -> UserGet:
    try:
        return await auth_service.get_me(session_id)
    except SessionNotFound as e:
        raise HTTPException(401, "Unauthorized")