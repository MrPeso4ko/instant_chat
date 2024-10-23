from fastapi import APIRouter

from api.auth import auth_router
from api.chats import chat_router

root_router = APIRouter(prefix="/api")

root_router.include_router(auth_router)
root_router.include_router(chat_router)